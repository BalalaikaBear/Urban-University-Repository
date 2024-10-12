from chunks import Chunk, ChunkState
from chunkdata import ChunksData
from hexclass import Hex
from cellclass import Cell, Biomes

from queue import Queue

class Map:
    def __init__(self) -> None:
        self.chunks: ChunksData = ChunksData(INIT={Hex(0, 0): Chunk(Hex(0, 0))})
        self.last_chunk: Chunk = self.chunks.INIT[Hex(0, 0)]

        # очереди
        self.source: Queue = Queue()
        self.frontier: Queue = Queue()

        # состояние
        self.working: bool = False

        # если центральный чанк еще не сгенерирован -> отправить его в очередь
        if self.last_chunk.state is ChunkState.INIT:
            self.source.put(self.last_chunk)

    def update(self) -> None:
        """Обновление очереди на генерацию чанков и их обновление"""
        # запуск генерации требуемого чанка
        if not self.working:
            # основной чанк
            if not self.source.empty():
                self.working = True
                self.last_chunk: Chunk = self.source.get()
                print(f'getting chunk from source: {self.last_chunk.coordinate}')

                # если данный чанк еще не был сгенерирован -> сгенерировать
                if self.last_chunk.coordinate not in self.chunks.FREEZE:
                    self.chunks.move(self.last_chunk)  # перенос информации из словаря INIT в словарь RELAXING
                    self.last_chunk.run()  # запуск генерации чанка

                # добавление соседних чанков в очередь на генерацию
                for near_chunk_coord in self.last_chunk.coordinate.neighbors():
                    if near_chunk_coord not in self.chunks:
                        new_chunk: Chunk = Chunk(near_chunk_coord)      # 1. создание нового чанка
                        self.chunks.INIT[near_chunk_coord] = new_chunk  # 2. добавление его в словарь
                        self.frontier.put(new_chunk)                    # 3. добавление его в очередь на генерацию

            # соседний чанк
            elif not self.frontier.empty():
                self.working = True
                self.last_chunk: Chunk = self.frontier.get()
                print(f'getting chunk from frontier: {self.last_chunk.coordinate}')
                self.chunks.move(self.last_chunk) # перенос информации из словаря INIT в словарь RELAXING
                self.last_chunk.run()  # запуск генерации чанка

        # процесс релаксации сетки каждый кадр
        if self.last_chunk.relax_iter < 100:
            self.last_chunk.update()
        elif self.last_chunk.state is ChunkState.RELAXING and self.last_chunk.relax_iter >= 100:
            self.last_chunk.freeze()

        # обновление состояния о работе генерации
        if self.last_chunk.state is ChunkState.FREEZE:
            # перенос информации из словаря RELAXING в словарь FREEZE
            if self.last_chunk.coordinate not in self.chunks.FREEZE:
                print(f'moving from RELAXING to FREEZE chunk {self.last_chunk.coordinate}')
                self.chunks.move(self.last_chunk, _from=ChunkState.RELAXING)
            self.working = False

    def add(self, pos: Hex) -> None:
        """Добавление чанка в очередь генерации"""
        if pos in self.chunks.FREEZE:
            self.source.put(self.chunks.FREEZE[pos])
        elif pos not in self.chunks:
            new_chunk = Chunk(pos)
            self.chunks.INIT[pos] = new_chunk
            self.source.put(new_chunk)



if __name__ == '__main__':
    game_map = Map()
