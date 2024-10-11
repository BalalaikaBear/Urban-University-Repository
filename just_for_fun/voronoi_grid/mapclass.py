from chunks import ChunkGrid, ChunkState
from hexclass import Hex
from cellclass import Cell, Biomes

from queue import Queue

class Map:
    def __init__(self) -> None:
        self.chunks: dict[Hex, ChunkGrid] = {Hex(0, 0): ChunkGrid(Hex(0, 0))}
        self.last_chunk: ChunkGrid = self.chunks[Hex(0, 0)]
        self.source: Queue = Queue()
        self.source_out: bool = True
        self.frontier: Queue = Queue()

        # если центральный чанк еще не сгенерирован -> отправить его в очередь
        if self.last_chunk.state is ChunkState.INIT:
            self.source.put(self.last_chunk)

    def update(self) -> None:
        # вытащить чанк из очереди
        if self.source_out and not self.source.empty():
            self.last_chunk: ChunkGrid = self.source.get()
            self.last_chunk.run()  # запуск генерации чанка
            self.source_out = False

        # создание новых чанков вокруг только что созданного чанка и добавление следующего генерируемого чанка в очередь
        if self.last_chunk.state is ChunkState.FREEZE:
            self.source_out = True
            # определение соседних координат
            for near_coord in self.last_chunk.coordinate.neighbors():
                if near_coord not in self.chunks:
                    new_chunk: ChunkGrid = ChunkGrid(near_coord)  # 1. создание нового чанка
                    self.chunks[near_coord] = new_chunk           # 2. добавление его в словарь
                    self.source.put(new_chunk)                    # 3. добавление его в очередь на генерацию

        # процесс релаксации сетки каждый кадр
        if self.last_chunk.relax_iter < 100:
            self.last_chunk.update()
        elif self.last_chunk.state is ChunkState.RELAXING and self.last_chunk.relax_iter >= 100:
            self.last_chunk.freeze()


if __name__ == '__main__':
    game_map = Map()
