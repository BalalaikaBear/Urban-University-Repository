import queue

from chunks import ChunkGrid, ChunkState
from hexclass import Hex
import pygame, sys
from queue import Queue

WIDTH = 1600
HEIGHT = 1200
size = 25

# инициализация
pygame.init()
running = True

# цвета
BACKGROUND = pygame.color.Color(200, 200, 200)

# настройки стандартных элементов pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def check_events() -> None:
    """Фиксация нажатия клавиш"""
    global running

    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            running = False

def draw() -> None:
    """Рисование объектов на экране"""
    for coordinate, chunk in chunk_map.items():
        if chunk.state > ChunkState.INIT:
            # центры ячеек
            for point in chunk.points:
                pygame.draw.circle(screen, (0, 0, 255),
                                   (point[0]*size + WIDTH/2, point[1]*size + HEIGHT/2), 1)

            # вершины ячеек
            for vor_point in chunk.vor.vertices:
                pygame.draw.circle(screen, (255, 0, 0),
                                   (vor_point[0] * size + WIDTH / 2, vor_point[1] * size + HEIGHT / 2), 1)

            # сегменты
            for segment in chunk.vor.regions:
                if segment and -1 not in segment:
                    pygame.draw.lines(screen, (140, 90, 200), True,
                                      [(chunk.vor.vertices[i][0] * size + WIDTH / 2,
                                        chunk.vor.vertices[i][1] * size + HEIGHT / 2)
                                       for i in segment])

if __name__ == '__main__':
    chunk = ChunkGrid(Hex(0, 0))
    chunks: list = [chunk]

    # данные о карте
    hex1: Hex = Hex(0, 0)
    chunk_map: dict = {hex1: chunk}

    # очередь
    gen_queue: queue.Queue = Queue()
    gen_queue.put(chunk)
    pull_out = True

    # вечно-обновляющийся цикл
    while running:
        clock.tick()

        check_events()

        screen.fill(BACKGROUND)
        draw()

        # вытащить чанк из очереди
        if pull_out and not gen_queue.empty():
            chunk: ChunkGrid = gen_queue.get()
            chunk.run()
            pull_out = False

        # создание новых чанков вокруг только что созданного чанка и добавление следующего генерируемого чанка в очередь
        if chunk.state is ChunkState.FREEZE:
            pull_out = True
            # определение соседних координат
            for near_coord in chunk.coordinate.neighbors():
                if near_coord not in chunk_map:
                    new_chunk: ChunkGrid = ChunkGrid(near_coord)  # 1. создание нового чанка
                    chunk_map[near_coord] = new_chunk             # 2. добавление его в словарь
                    gen_queue.put(new_chunk)                      # 3. добавление его в очередь на генерацию

        # процесс релаксации сетки каждый кадр
        if chunk.relax_iter < 100:
            chunk.update()
        elif chunk.state is ChunkState.RELAXING and chunk.relax_iter >= 100:
            chunk.freeze()

        #print("FPS:", clock.get_fps())
        pygame.display.update()

    # закрытие программы
    pygame.quit()
    sys.exit()
