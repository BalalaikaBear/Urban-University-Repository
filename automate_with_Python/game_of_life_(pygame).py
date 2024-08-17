import pygame
import random

pygame.init()

# COLORS
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# GRID SIZES
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()  # контроль времени


def gen(num):
    """
    Генерация ячеек при их заданном количестве
    """
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])


def draw_grid(positions, playing):
    """
    Отрисовка поля ячеек
    """
    for position in positions:  # отрисовка живых ячеек
        col, row = position  # x, y
        top_left = (col * TILE_SIZE, row * TILE_SIZE)  # координата квадрата
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))  # (<x>, <y>, <ширина>, <высота>)

    for row in range(GRID_HEIGHT):  # горизонтальные линии
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):  # вертикальные линии
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

    if not playing:  # отрисовка рамок во время паузы
        pygame.draw.rect(screen, RED, (0, 0, WIDTH, HEIGHT), 2)


def adjust_grid(positions):
    """
    Перерасчет всех ячеек
    """
    all_neighbors = set()  # ячейки с хотя бы одним соседом
    new_positions = set()  # подготовка ячеек для следующего кадра

    # отфильтровка еще живых ячеек
    for position in positions:
        neighbors = get_neighbors(position)  # соседние ячейки
        all_neighbors.update(neighbors)  # добавление соседей в общее множество

        neighbors = list(filter(lambda x: x in positions, neighbors))  # вывод только живых ячеек

        # ячейка имеет 2 или 3 соседа?
        if len(neighbors) in [2, 3]:
            new_positions.add(position)  # ячейка остается на месте

    # создание новых ячеек
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))  # вывод только живых ячеек

        if len(neighbors) == 3:
            new_positions.add(position)

    return new_positions


def get_neighbors(pos):
    """
    Возвращает множество соседей у заданной ячейки
    """
    x, y = pos
    neighbours = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > GRID_WIDTH:  # не учитывать ячейки за краем экрана
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > GRID_HEIGHT:  # не учитывать ячейки за краем экрана
                continue

            if dx == 0 and dy == 0:  # игнорировать центральную ячейку (себя)
                continue

            neighbours.append((x + dx, y + dy))

    return neighbours


def main():
    running = True
    playing = False

    count = 0
    update_freq = 10  # частота обновления ячеек (кадры)

    is_mouse_pressed = False
    pressed_pos = set()

    positions = set()

    # Основной цикл
    while running:
        clock.tick(FPS)  # вычисляет сколько миллисекунд прошло с прошлого кадра

        if playing:  # обновляет счетчик обновления ячеек каждый кадр
            count += 1

        if count >= update_freq:  # производить перерасчет ячеек с заданной частотой
            count = 0
            positions = adjust_grid(positions)

        # изменяет название окна при паузе
        pygame.display.set_caption("Simulation playing" if playing else "Simulation paused")

        for event in pygame.event.get():
            # возможность закрыть приложение
            if event.type == pygame.QUIT:
                running = False

            # редактирование ячеек нажатием мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_mouse_pressed = True

                # вычисление позиции курсора
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                # смена статуса ячейки
                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

                pressed_pos.add(pos)

            # редактирование ячеек удержанием мыши
            if event.type == pygame.MOUSEMOTION and is_mouse_pressed:
                # вычисление позиции курсора
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                # смена статуса ячейки
                if pos not in pressed_pos:
                    if pos in positions:
                        positions.remove(pos)
                    else:
                        positions.add(pos)

                pressed_pos.add(pos)

            # отжатие мыши
            if event.type == pygame.MOUSEBUTTONUP:
                is_mouse_pressed = False
                pressed_pos = set()

            if event.type == pygame.KEYDOWN:
                # space - пауза
                if event.key == pygame.K_SPACE:
                    playing = not playing

                # clear - очистка поля
                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0

                # generate - генерация случайного поля
                if event.key == pygame.K_g:
                    # в каждой колонне примерно от ... до ... ячеек
                    positions = gen(random.randrange(5, 10) * GRID_WIDTH)

        screen.fill(GREY)  # цвет фона приложения
        draw_grid(positions, playing)  # функция отрисовки
        pygame.display.update()  # обновление экрана каждый кадр

    pygame.quit()


if __name__ == "__main__":
    main()
