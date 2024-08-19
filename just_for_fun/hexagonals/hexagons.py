import random

import pygame, math
from collections import namedtuple

# инициализация
pygame.init()
pygame.font.init()

# типы данных
Color = namedtuple("Color", ["r", "g", "b"])
Hex = namedtuple("Hex", ["q", "r"])  # axial storage
Point = namedtuple("Point", ["x", "y"])
HEX_DIRECTIONS = [Hex(1, 0), Hex(1, -1), Hex(0, -1), Hex(-1, 0), Hex(-1, 1), Hex(0, 1)]  # соседние ячейки по часовой стрелке

# цвета
BACKGROUND = Color(200, 200, 200)
WHITE = Color(255, 255, 255)

# размер экрана
WIDTH = 1000
HEIGHT = 1000
HEXAGON_SIZE = 50
FPS = 60
running = True

class Camera:
    def __init__(self, pos_speed=2, position=[0,0], rotation=0.0, zoom=0.0):
        self.pos_speed = pos_speed
        self.position = position
        self.rotation = rotation
        self.zoom = zoom
        self.dx = 0
        self.dy = 0

    def update(self):
        """Перемещение камеры на заданное значение"""
        self.position[0] += self.dx * self.pos_speed
        self.position[1] += self.dy * self.pos_speed


camera = Camera()

# настройки стандартных элементов pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)

# Hexagonal math
def hex_add(a: Hex, b: Hex):
    """Сложение координат ячеек"""
    return Hex(a.q + b.q, a.r + b.r)

def hex_sub(a: Hex, b: Hex):
    """Вычитание координат ячеек"""
    return Hex(a.q - b.q, a.r - b.r)

def hex_multi(a: Hex, b: Hex):
    """Умножение координат ячеек"""
    return Hex(a.q * b.q, a.r * b.r)

def hex_length(hexagon: Hex):
    """Расстояние до ячейки"""
    return int((abs(hexagon.q) + abs(hexagon.r)) / 2)

def hex_distance(a: Hex, b: Hex):
    """Расстояние между двумя ячейками"""
    return hex_length(hex_sub(a, b))

def hex_direction(direction: int):
    """Возвращает ячейку в зависимости от введенного направления"""
    return HEX_DIRECTIONS[direction]

def hex_neighbor(hexagon: Hex, direction: int):
    """Возвращает следующую ячейку вдоль направления"""
    return hex_add(hexagon, hex_direction(direction))

class Orientation:
    """Хранит информацию о поворотных матриц и угол поворота ячеек"""
    def __init__(self, f0, f1, f2, f3, b0, b1, b2, b3, start_angle):
        # матрица поворота
        self.f0 = f0
        self.f1 = f1
        self.f2 = f2
        self.f3 = f3

        # обратная матрица поворота
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3

        # начальный угол поворота ячеек
        self.start_angle = start_angle


# стартовая ориентация ячеек
layout_flat = Orientation(3/2, 0, math.sqrt(3)/2, math.sqrt(3),
                          2/3, 0, -1/3, math.sqrt(3)/3,
                          0)

class Layout:
    """Хранит информацию об изначальной ориентации ячеек, их размер, и начало координат"""
    def __init__(self, start_orientation: Orientation, size, origin: Point):
        self.start_orientation = start_orientation
        self.size = size
        self.origin = origin


# применяемая система координат (перемещение, масштабирование, начальное положение)
LAYOUT = Layout(layout_flat, HEXAGON_SIZE, Point(WIDTH // 2, HEIGHT // 2))

def hex_to_pixel(layout: Layout, hexagon: Hex):
    """Переводит из шестиугольной (Hexagonal) системы координат в экранную (2D) систему координат """
    matrix = layout.start_orientation  # матрицы поворота
    size = layout.size  # размер ячеек
    origin = layout.origin  # начало координат

    # перемножение матриц
    x = (matrix.f0 * hexagon.q + matrix.f1 * hexagon.r) * size
    y = (matrix.f2 * hexagon.q + matrix.f3 * hexagon.r) * size

    return Point(x + origin.x, y + origin.y)

def pixel_to_hex(layout: Layout, pixel: Point):
    """Переводит из экранной (2D) системы координат в шестиугольную (Hexagonal) систему координат"""
    matrix = layout.start_orientation  # матрицы поворота
    size = layout.size  # размер ячеек
    origin = layout.origin  # начало координат

    # перемножение матриц
    pt = Point((pixel.x - origin.x) / size, (pixel.y - origin.y) / size)
    q = matrix.b0 * pt.x + matrix.b1 * pt.y
    r = matrix.b2 * pt.x + matrix.b3 * pt.y

    return Hex(q, r)

class HexCell:
    def __init__(self, coordinate, color=Color(255, 192, 203)):
        self.coordinate = coordinate
        self.color = color

    def draw(self, screen, position, size):
        pygame.draw.circle(screen, self.color, position, size)
        pygame.draw.lines(screen, (0, 0, 0), True, self.pixels_corners(position, size))

    def pixels_corners(self, position, size):
        corners = []
        x, y = position

        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg
            corners.append((x + size * math.cos(angle_rad), y + size * math.sin(angle_rad)))

        return corners


def check_events():
    """Управление"""
    global running

    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                camera.dx = -1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                camera.dx = 1
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                camera.dy = -1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                camera.dy = 1

        if event.type == pygame.KEYUP:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                camera.dx = 0
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                camera.dx = 0
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                camera.dy = 0
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                camera.dy = 0

def draw_grid(coordinates):
    """Отрисовка ячеек на экране"""
    show_coord = True  # отображение координат шестиугольников

    # ОТРИСОВКА ЯЧЕЕК
    for coordinate, hexagon in coordinates.items():
        position = hex_to_pixel(LAYOUT, hexagon.coordinate)  # положение на экране
        hexagon.draw(screen, position, HEXAGON_SIZE)  # отрисовка шестиугольника

        if show_coord:  # отображение координат шестиугольников
            coord_text = font.render("{}, {}".format(*coordinate), False, WHITE)
            coord_text_rect = coord_text.get_rect()
            coord_text_rect.center = position
            screen.blit(coord_text, coord_text_rect)

def main():

    # координаты существующих шестиугольников
    coordinates = {}

    # генератор сетки
    for i in range(-4, 5):
        for j in range(-4, 5):
            pos = Hex(i, j)
            coordinates[pos] = HexCell(pos, (random.randint(0, 255),
                                             random.randint(0, 255),
                                             random.randint(0, 255)))

    while running:
        clock.tick(FPS)

        check_events()  # управление и ивенты

        # ОТРИСОВКА И ОБНОВЛЕНИЕ ЭКРАНА
        screen.fill(BACKGROUND)
        draw_grid(coordinates)
        pygame.display.update()
        print(camera.position)
        camera.update()

    pygame.quit()


def test():
    def complain(name):
        print("FAIL {0}".format(name))

    def equal_hex(name, a, b):
        if not (a.q == b.q and a.r == b.r):
            complain(name)

    def test_math():
        equal_hex("hex_add", Hex(10, 5), hex_add(Hex(5, 7), Hex(5, -2)))
        equal_hex("hex_sub", Hex(10, 5), hex_sub(Hex(12, 3), Hex(2, -2)))
        equal_hex("hex_mul", Hex(10, 6), hex_multi(Hex(5, 3), Hex(2, 2)))

    test_math()


if __name__ == "__main__":
    test()
    main()
