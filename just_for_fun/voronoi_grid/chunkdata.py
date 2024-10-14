from chunks import ChunkGen, ChunkState
from hexclass import Hex
from typing import Optional

class ChunksData:
    def __init__(self, **kwargs) -> None:
        self.INIT = {}
        self.RELAXING = {}
        self.FREEZE = {}
        self.GEN_CELLS = {}
        self.DONE = {}

        for key, value in kwargs.items():
            if key == 'INIT':
                self.INIT = value
            if key == 'RELAXING':
                self.RELAXING = value
            if key == 'FREEZE':
                self.FREEZE = value
            if key == 'GEN_CELLS':
                self.GEN_CELLS = value
            if key == 'DONE':
                self.DONE = value

    @property
    def size(self) -> int:
        """Возвращает количество чанков в объекте"""
        return (len(self.INIT) +
                len(self.RELAXING) +
                len(self.FREEZE) +
                len(self.GEN_CELLS) +
                len(self.DONE))

    def move(self, inp: ChunkGen | Hex, _from: Optional[ChunkState] = None) -> None:
        if isinstance(inp, ChunkGen):
            if _from is None:
                state = inp.state
            else:
                state = _from

            if state is ChunkState.INIT:
                self.RELAXING[inp.coordinate] = self.INIT.pop(inp.coordinate)
            elif state is ChunkState.RELAXING:
                self.FREEZE[inp.coordinate] = self.RELAXING.pop(inp.coordinate)
            elif state is ChunkState.FREEZE:
                self.GEN_CELLS[inp.coordinate] = self.FREEZE.pop(inp.coordinate)
            elif state is ChunkState.GEN_CELLS:
                self.DONE[inp.coordinate] = self.GEN_CELLS.pop(inp.coordinate)
            else:
                raise ValueError('Cannot move chunk to higher dict')

        elif isinstance(inp, Hex):
            if _from is None:
                state = inp
            else:
                state = _from

            if state is ChunkState.INIT:
                self.RELAXING[inp] = self.INIT.pop(inp)
            elif state is ChunkState.RELAXING:
                self.FREEZE[inp] = self.RELAXING.pop(inp)
            elif state is ChunkState.FREEZE:
                self.GEN_CELLS[inp] = self.FREEZE.pop(inp)
            elif state is ChunkState.GEN_CELLS:
                self.DONE[inp] = self.GEN_CELLS.pop(inp)
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
    chunk_data = ChunksData(INIT={Hex(0, 0): ChunkGen(Hex(0, 0))})
    print(chunk_data.INIT, chunk_data.RELAXING)
    print(chunk_data)
