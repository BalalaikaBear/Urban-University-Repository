import multiprocessing
import numpy as np
import math
from datetime import datetime

# With multiprocessing: 0:00:22.157997 [1.5e+03 0.0e+00 1.0e+00]
# Without multiprocessing: 0:00:26.870035 [1.5e+03 0.0e+00 1.0e+00]


sqrt3 = math.sqrt(3)
orientation = np.array([[3 / 2, 0, 0],
                        [sqrt3 / 2, sqrt3, 0],
                        [0, 0, 1]])


def matrix_basis(points):
    return np.array([points[0], points[1], 1]) @ orientation


if __name__ == '__main__':  # необходимо, чтобы мультипроцесс не запускал сам себя
    positions = [(x, y) for x in range(3000) for y in range(3000)]

    start = datetime.now()
    # использование нескольких процессов (ядер)
    with multiprocessing.Pool(processes=4) as pool:  # <processes> - количество процессов (ядер)

        # аналогично map, но разбиением на процессы (ядра)
        A = pool.map(matrix_basis, positions)
        # 1-й аргумент - функция
        # 2+ аргументы - итерируемые объекты, поступающие в функцию

    end = datetime.now()
    print('With multiprocessing:', end - start, A[len(positions) // 3])

    start = datetime.now()
    # использование одного потока
    B = list(map(matrix_basis, positions))
    end = datetime.now()
    print('Without multiprocessing:', end - start, B[len(positions) // 3])
