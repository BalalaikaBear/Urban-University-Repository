from chunks import Chunk, ChunkState
from hexclass import Hex
from typing import Optional

class ChunksData:
    def __init__(self, **kwargs) -> None:
        INIT = True
        RELAXING = True
        FREEZE = True
        GEN_CELLS = True
        DONE = True

        for key, value in kwargs.items():
            if key == 'INIT':
                self.INIT = value
                INIT = False
            if key == 'RELAXING':
                self.RELAXING = value
                RELAXING = False
            if key == 'FREEZE':
                self.FREEZE = value
                FREEZE = False
            if key == 'GEN_CELLS':
                self.GEN_CELLS = value
                GEN_CELLS = False
            if key == 'DONE':
                self.DONE = value
                DONE = False

        if INIT: self.INIT = {}
        if RELAXING: self.RELAXING = {}
        if FREEZE: self.FREEZE = {}
        if GEN_CELLS: self.GEN_CELLS = {}
        if DONE: self.DONE = {}

    @property
    def size(self) -> int:
        """Возвращает количество чанков в объекте"""
        return (len(self.INIT) +
                len(self.RELAXING) +
                len(self.FREEZE) +
                len(self.GEN_CELLS) +
                len(self.DONE))

    def move(self, input: Chunk | Hex, _from: Optional[ChunkState] = None) -> None:
        if isinstance(input, Chunk):
            if _from is None:
                state = input.state
            else:
                state = _from

            if state is ChunkState.INIT:
                self.RELAXING[input.coordinate] = self.INIT.pop(input.coordinate)
            elif state is ChunkState.RELAXING:
                self.FREEZE[input.coordinate] = self.RELAXING.pop(input.coordinate)
            elif state is ChunkState.FREEZE:
                self.GEN_CELLS[input.coordinate] = self.FREEZE.pop(input.coordinate)
            elif state is ChunkState.GEN_CELLS:
                self.DONE[input.coordinate] = self.GEN_CELLS.pop(input.coordinate)
            else:
                raise ValueError('Cannot move chunk to higher dict')

        elif isinstance(input, Hex):
            if _from is None:
                state = input
            else:
                state = _from

            if state is ChunkState.INIT:
                self.RELAXING[input] = self.INIT.pop(input)
            elif state is ChunkState.RELAXING:
                self.FREEZE[input] = self.RELAXING.pop(input)
            elif state is ChunkState.FREEZE:
                self.GEN_CELLS[input] = self.FREEZE.pop(input)
            elif state is ChunkState.GEN_CELLS:
                self.DONE[input] = self.GEN_CELLS.pop(input)
            else:
                raise ValueError('Cannot move chunk to higher dict')

    def __contains__(self, item):
        if item in self.INIT: return True
        elif item in self.RELAXING: return True
        elif item in self.FREEZE: return True
        elif item in self.GEN_CELLS: return True
        elif item in self.DONE: return True
        else: return False

    def __str__(self) -> str:
        return (
            f'ChunkData(SIZE={self.size}, [' +
            f'INIT: {len(self.INIT)}, ' +
            f'RELAXING: {len(self.RELAXING)}, ' +
            f'FREEZE: {len(self.FREEZE)}, ' +
            f'GEN_CELLS: {len(self.GEN_CELLS)}, ' +
            f'DONE: {len(self.DONE)}])'
        )

if __name__ == '__main__':
    chunk_data = ChunksData(INIT={Hex(0, 0): Chunk(Hex(0, 0))})
    print(chunk_data.INIT, chunk_data.RELAXING)
    print(chunk_data)
