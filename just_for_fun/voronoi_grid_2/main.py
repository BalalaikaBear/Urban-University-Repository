from just_for_fun.voronoi_grid_2.generators.chunk import ChunkGen, ChunkState
from just_for_fun.voronoi_grid_2.generators.mapgen import MapGen
from just_for_fun.voronoi_grid_2.classes.cells_data import CellsMap
from just_for_fun.voronoi_grid_2.classes.hexclass import Hex
import pygame, sys

WIDTH = 1600
HEIGHT = 1200
size = 35

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
    for coordinate, chunk in map_gen.chunks_dict.items():
        if ChunkState.INIT < chunk.state < ChunkState.GEN_CELLS:
            # центры ячеек
            for point in chunk.points:
                pygame.draw.circle(screen,
                                   (0, 0, 255),
                                   (point[0] * size + WIDTH / 2, point[1] * size + HEIGHT / 2),
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

        elif chunk.state >= ChunkState.GEN_CELLS:
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
            # центры ячеек
            for point in chunk.points:
                pygame.draw.circle(screen,
                                   (50, 150, 255),
                                   (point[0] * size + WIDTH / 2, point[1] * size + HEIGHT / 2),
                                   1)


if __name__ == '__main__':
    map_gen: MapGen = MapGen(map_data=CellsMap())
    frame = 0

    # вечно-обновляющийся цикл
    while running:
        clock.tick()
        frame += 1

        check_events()

        screen.fill(BACKGROUND)
        draw()
        map_gen.update()

        if frame == 100:
            print('NEW CHUNK')
            map_gen.add(Hex(0, 1))

        #print("FPS:", clock.get_fps())
        pygame.display.update()

    # закрытие программы
    pygame.quit()
    sys.exit()
