from chunks import ChunkGen, ChunkState
from hexclass import Hex
from mapclass import MapGen
import pygame, sys

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
    for coordinate, chunk in map_data.chunks.FREEZE.items():
        if chunk.states > ChunkState.INIT:
            # сегменты
            for segment in chunk.vor.regions:
                if segment and -1 not in segment:
                    pygame.draw.lines(screen,
                                      (150, 150, 180),
                                      True,
                                      [(chunk.vor.vertices[i][0] * size + WIDTH / 2,
                                        chunk.vor.vertices[i][1] * size + HEIGHT / 2)
                                       for i in segment])
            for simpl in chunk.dl.simplices:
                pygame.draw.lines(screen,
                                  (190, 190, 190),
                                  True,
                                  [(chunk.dl.points[i][0] * size + WIDTH / 2,
                                    chunk.dl.points[i][1] * size + HEIGHT / 2)
                                   for i in simpl])

    for coordinate, chunk in map_data.chunks.RELAXING.items():
        if chunk.states > ChunkState.INIT:
            # центры ячеек
            for point in chunk.points:
                pygame.draw.circle(screen,
                                   (0, 0, 255),
                                   (point[0]*size + WIDTH/2, point[1]*size + HEIGHT/2),
                                   1)

            # вершины ячеек
            for vor_point in chunk.vor.vertices:
                pygame.draw.circle(screen,
                                   (255, 0, 0),
                                   (vor_point[0] * size + WIDTH / 2, vor_point[1] * size + HEIGHT / 2),
                                   1)

            # сегменты
            for segment in chunk.vor.regions:
                if segment and -1 not in segment:
                    pygame.draw.lines(screen,
                                      (140, 90, 200),
                                      True,
                                      [(chunk.vor.vertices[i][0] * size + WIDTH / 2,
                                        chunk.vor.vertices[i][1] * size + HEIGHT / 2)
                                       for i in segment])


if __name__ == '__main__':
    map_data: MapGen = MapGen()
    frame = 0

    # вечно-обновляющийся цикл
    while running:
        clock.tick()
        frame += 1

        check_events()

        screen.fill(BACKGROUND)
        draw()
        map_data.update()

        if frame == 600:
            print('NEW CHUNK')
            map_data.add(Hex(0, 1))

        #print("FPS:", clock.get_fps())
        pygame.display.update()

    # закрытие программы
    pygame.quit()
    sys.exit()
