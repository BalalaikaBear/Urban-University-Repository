from chunks import ChunkGrid
import pygame, sys

WIDTH = 1600
HEIGHT = 1200
size = 8

# инициализация
pygame.init()
running = True

# цвета
BACKGROUND = pygame.color.Color(200, 200, 200)

# настройки стандартных элементов pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def check_events() -> None:
    global running

    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            running = False

def draw() -> None:
    for chunk in chunks:
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
            if segment and not -1 in segment:
                pygame.draw.lines(screen, (140, 90, 200), True,
                                  [(chunk.vor.vertices[i][0] * size + WIDTH / 2,
                                    chunk.vor.vertices[i][1] * size + HEIGHT / 2)
                                   for i in segment if i != -1])

if __name__ == '__main__':
    chunk = ChunkGrid((0, 0))
    chunk2 = ChunkGrid((1, 1))
    chunks = (chunk, chunk2)

    while running:
        clock.tick()

        check_events()

        screen.fill(BACKGROUND)
        draw()
        for chunk in chunks:
            chunk.update()
        pygame.display.update()

    pygame.quit()
    sys.exit()
