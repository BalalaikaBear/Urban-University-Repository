from just_for_fun.voronoi_grid_2.generators.chunk import ChunkGen, ChunkState
from just_for_fun.voronoi_grid_2.classes.hexclass import Hex
from just_for_fun.voronoi_grid_2.classes.cellclass import Cell, Biomes

from queue import Queue
from enum import IntEnum, auto

class ChunkType(IntEnum):
    """Информация об обязательной генерации чанка"""
    REQUIRED = auto()  # обязательная полностью сгенерированная ячейка
    OUTSKIRTS = auto()  # генерировать до состояния FREEZE

class MapGen:
    def __init__(self) -> None:
        # очередь генерации
        chunk = ChunkGen(Hex(0, 0))
        self.chunks: set = {Hex(0, 0)}
        self.chunks_dict: dict = {Hex(0, 0): chunk}  # дополнительный словарь с чанками (временное)
        self.last_chunk: ChunkGen = chunk
        self.frontier: Queue = Queue()

        # состояние
        self.working: bool = False

        # если центральный чанк еще не сгенерирован -> отправить его в очередь
        if self.last_chunk.state is ChunkState.INIT:
            self.frontier.put((ChunkType.REQUIRED,
                               self.last_chunk))

    def update(self) -> None:
        """Обновление очереди на генерацию чанков и их обновление"""
        # запуск генерации требуемого чанка
        if not self.working and not self.frontier.empty():
            is_required, self.last_chunk = self.frontier.get()
            self.working = True

            self.last_chunk.run()  # запуск генерации чанка

            # добавление соседних чанков в очередь на генерацию
            if is_required is ChunkType.REQUIRED:
                self._call_neighbors()

        # процесс релаксации сетки каждый кадр
        if self.last_chunk.relax_iter < 30:
            self.last_chunk.update()
        elif self.last_chunk.state is ChunkState.RELAXING and self.last_chunk.relax_iter >= 30:
            self.last_chunk.freeze()
            self.working = False

    def _call_neighbors(self, chunk: ChunkGen = None) -> None:
        """Добавление соседних чанков в очередь на генерацию"""
        if chunk is None:
            last_chunk = self.last_chunk
        else:
            last_chunk = chunk
        for near_chunk_coord in last_chunk.coordinate.neighbors():
            if near_chunk_coord not in self.chunks:
                # 1. создание нового чанка
                new_chunk: ChunkGen = ChunkGen(near_chunk_coord)
                # 2. добавление его в множество
                self.chunks.add(new_chunk.coordinate)
                self.chunks_dict[new_chunk.coordinate] = new_chunk  # дополнительный словарь с чанками (временное)
                # 3. добавление его в очередь на генерацию
                self.frontier.put((ChunkType.OUTSKIRTS, new_chunk))

    def add(self, pos: Hex) -> None:
        """Добавление чанка в очередь генерации"""
        if pos in self.chunks:
            self._call_neighbors()
        else:
            new_chunk = ChunkGen(pos)
            self.chunks.add(new_chunk.coordinate)
            self.chunks_dict[new_chunk.coordinate] = new_chunk  # дополнительный словарь с чанками (временное)
            self.frontier.put((ChunkType.REQUIRED, new_chunk))


if __name__ == '__main__':
    game_map = MapGen()
    game_map.update()
