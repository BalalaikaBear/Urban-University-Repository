from chunks import Chunk, ChunkState
from chunkdata import ChunksData
from hexclass import Hex
from cellclass import Cell, Biomes

from queue import PriorityQueue
from enum import StrEnum, auto

class ChunkType(StrEnum):
    """Информация об обязательной генерации чанка"""
    REQUIRED = auto()  # обязательная полностью сгенерированная ячейка
    OUTSKIRTS = auto()  # генерировать до состояния FREEZE

class Map:
    def __init__(self) -> None:
        self.chunks: ChunksData = ChunksData(INIT={Hex(0, 0): Chunk(Hex(0, 0))})
        self.last_chunk: Chunk = self.chunks.INIT[Hex(0, 0)]

        # очереди
        self.frontier: PriorityQueue = PriorityQueue()
        self.queue_id: int = 0

        # состояние
        self.working: bool = False

        # если центральный чанк еще не сгенерирован -> отправить его в очередь
        if self.last_chunk.state is ChunkState.INIT:
            self.frontier.put((ChunkState.INIT, self.queue_id, ChunkType.REQUIRED, self.last_chunk))

    def update(self) -> None:
        """Обновление очереди на генерацию чанков и их обновление"""
        # запуск генерации требуемого чанка
        if not self.working and not self.frontier.empty():
            state, q_id, how_gen, self.last_chunk = self.frontier.get()
            self.queue_id += 1
            self.working = True
            print(f'Generating CHUNK {str(self.last_chunk.coordinate):10} ' +
                  f'in state {str(state.name):10} with priority {str(how_gen.name):10}')

            # если данный чанк еще не был сгенерирован -> сгенерировать
            if self.last_chunk.coordinate in self.chunks.INIT:
                self.chunks.move(self.last_chunk)  # перенос информации из словаря INIT в словарь RELAXING
                self.last_chunk.run()  # запуск генерации чанка
                self.frontier.put((ChunkState.RELAXING, self.queue_id, how_gen, self.last_chunk))

                # добавление в очередь для финальной генерации
                if how_gen == ChunkType.REQUIRED:
                    self.frontier.put((ChunkState.FREEZE, self.queue_id, ChunkType.REQUIRED, self.last_chunk))

            # если чанк еще на этапе релаксации -> вернуть в очередь
            if state is ChunkState.RELAXING:
                self.frontier.put((self.last_chunk.state, self.queue_id, how_gen, self.last_chunk))

            if how_gen == ChunkType.REQUIRED:
                # добавление соседних чанков в очередь на генерацию
                for near_chunk_coord in self.last_chunk.coordinate.neighbors():
                    if near_chunk_coord not in self.chunks:
                        # 1. создание нового чанка
                        new_chunk: Chunk = Chunk(near_chunk_coord)
                        # 2. добавление его в словарь
                        self.chunks.INIT[near_chunk_coord] = new_chunk
                        # 3. добавление его в очередь на генерацию
                        self.frontier.put((ChunkState.INIT, self.queue_id, ChunkType.OUTSKIRTS, new_chunk))

        # процесс релаксации сетки каждый кадр
        if self.last_chunk.relax_iter < 100:
            self.last_chunk.update()
        elif self.last_chunk.state is ChunkState.RELAXING and self.last_chunk.relax_iter >= 100:
            self.last_chunk.freeze()

        # обновление состояния о работе генерации
        if self.last_chunk.state is ChunkState.FREEZE:
            # перенос информации из словаря RELAXING в словарь FREEZE
            if self.last_chunk.coordinate not in self.chunks.FREEZE:
                self.chunks.move(self.last_chunk, _from=ChunkState.RELAXING)
            self.working = False

    def add(self, pos: Hex) -> None:
        """Добавление чанка в очередь генерации"""
        if pos in self.chunks.FREEZE:
            self.queue_id += 1
            self.frontier.put((ChunkState.FREEZE, self.queue_id, ChunkType.REQUIRED, self.chunks.FREEZE[pos]))
        elif pos not in self.chunks:
            new_chunk = Chunk(pos)
            self.chunks.INIT[pos] = new_chunk
            self.queue_id += 1
            self.frontier.put((ChunkState.INIT, self.queue_id, ChunkType.REQUIRED, new_chunk))


if __name__ == '__main__':
    game_map = Map()
