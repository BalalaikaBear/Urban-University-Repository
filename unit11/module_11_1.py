import multiprocessing
import numpy as np
import math
from datetime import datetime
from collections import namedtuple

# With multiprocessing: 0:00:03.930021 Point(x=np.float64(787.886459460218), y=np.float64(576.7729189204362))
# Without multiprocessing: 0:00:04.589978 Point(x=np.float64(787.886459460218), y=np.float64(576.7729189204362))


sqrt3 = math.sqrt(3)
Hex = namedtuple('Hex', ['q', 'r'])
Point = namedtuple('Point', ['x', 'y'])
orientation = np.array([[3 / 2, 0, 0],
                        [sqrt3 / 2, sqrt3, 0],
                        [0, 0, 1]])


def change_basis(position: Hex):
    matrix = np.array([position.q, position.r, 1]) @ orientation
    return Point(matrix[0], matrix[1])


if __name__ == '__main__':  # необходимо, чтобы мультипроцесс не запускал сам себя
    # создание списка координат
    positions: list[Hex] = [Hex(q, r) for q in range(1000) for r in range(1000)]

    # использование нескольких процессов
    start = datetime.now()
    with multiprocessing.Pool(processes=4) as pool:  # <processes> - количество процессов

        # аналогично map, но разбиением на процессы
        A: list[Point] = pool.map(change_basis, positions)
        # 1-й аргумент - функция
        # 2+ аргументы - итерируемые объекты, поступающие в функцию

    end = datetime.now()
    print('With multiprocessing:', end - start, A[len(positions) // 3])

    # использование одного потока
    start = datetime.now()
    B: list[Point] = list(map(change_basis, positions))
    end = datetime.now()
    print('Without multiprocessing:', end - start, B[len(positions) // 3])
