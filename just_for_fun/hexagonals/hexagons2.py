import pygame
import random, math, copy
import numpy as np
from numpy.linalg import inv
from collections import namedtuple

# инициализация
pygame.init()
pygame.font.init()

# типы данных
Color = namedtuple("Color", ["r", "g", "b"])
Hex = namedtuple("Hex", ["q", "r"])  # axial storage
Point = namedtuple("Point", ["x", "y"])
HEX_DIRECTIONS = [Hex(1, 0), Hex(1, -1), Hex(0, -1),
                  Hex(-1, 0), Hex(-1, 1), Hex(0, 1)]  # соседние ячейки по часовой стрелке

# цвета
BACKGROUND = Color(200, 200, 200)
WHITE = Color(255, 255, 255)

# размер экрана
WIDTH = 1600
HEIGHT = 900
BORDER = 150
ORIGIN = Point(WIDTH // 2, HEIGHT // 2)

# Константы
HEXAGON_SIZE = 50
FPS = 60
running = True
sqrt3 = math.sqrt(3)

# скорость перемещения камеры
CAMERA_SPEED = 12
ROTATION_SPEED = 1
SCALE_SPEED = 1/20

# проверка нажатия кнопок
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
turn_counterclockwise = False
turn_clockwise = False

# настройки стандартных элементов pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)

# слои экрана
layer_hex = pygame.Surface((WIDTH, HEIGHT))
layer_lines = pygame.Surface((WIDTH, HEIGHT))
layer_text = pygame.Surface((WIDTH, HEIGHT))

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

def hex_round(hexagon: Hex):
    """Возвращает ближайшую ячейку к точке"""
    q = int(round(hexagon.q))
    r = int(round(hexagon.r))
    s = int(round(-hexagon.q - hexagon.r))
    q_diff = abs(q - hexagon.q)
    r_diff = abs(r - hexagon.r)
    s_diff = abs(s + hexagon.q + hexagon.r)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r - s
    elif r_diff > s_diff:
        r = -q - s
    else:
        s = -q - r
    return Hex(q, r)

def lerp(a, b, t):
    """Линейная интерполяция между двумя точками"""
    return a + (b-a)*t

def hex_lerp(a: Hex, b: Hex, t):
    """Линейная интерполяция между двумя точками в шестиугольной системе координат"""
    return Hex(lerp(a.q, b.q, t), lerp(a.r, b.r, t))

def hex_linedraw(a: Hex, b: Hex):
    """Выводит список из положений ячеек, расположенных между двумя точками"""
    length = hex_distance(a, b)
    # добавление значение epsilon для смещения крайней точки
    a_nudge = Hex(a.q + 1e-06, a.r + 1e-06)
    b_nudge = Hex(b.q + 1e-06, b.r + 1e-06)
    results = []
    step = 1/max(length, 1)
    for i in range(0, length, step):
        results.append(hex_round(hex_lerp(a_nudge, b_nudge, i)))
    return results

# Системы координат
class Orientation:
    """Хранит информацию о матрицах поворота и угле поворота ячеек"""
    def __init__(self, a00, a01, a02, a10, a11, a12, b00, b01, b02, b10, b11, b12, angle):
        # матрица поворота
        self.a00 = a00
        self.a01 = a01
        self.a02 = a02
        self.a10 = a10
        self.a11 = a11
        self.a12 = a12

        # обратная матрица поворота
        self.b00 = b00
        self.b01 = b01
        self.b02 = b02
        self.b10 = b10
        self.b11 = b11
        self.b12 = b12

        # начальный угол поворота ячеек
        self.angle = angle

    def reverse(self):
        """Возвращает обратную матрицу"""
        self.b10 = self.a10 / (self.a01*self.a10 - self.a00*self.a11)
        self.b00 = -self.a11*self.b10/self.a10
        self.b11 = self.a00 / (self.a11*self.a00 - self.a10*self.a01)
        self.b01 = -self.a01*self.b11/self.a00
        self.b12 = (self.a10*self.a02 - self.a00*self.a12) / (self.a00*self.a11 - self.a10*self.a01)
        self.b02 = (-self.a02 - self.a01*self.b12) / self.a00

        return self.b00, self.b01, self.b02, self.b10, self.b11, self.b12


# стартовая ориентация ячеек
layout_flat = Orientation(3/2, 0, 0, sqrt3/2, sqrt3, 0,
                          2/3, 0, 0, -1/3, sqrt3/3, 0,
                          0)

class Layout:
    """Система координат"""
    def __init__(self, start_orientation: Orientation, size):
        self.orientation = copy.copy(start_orientation)  # матрица поворота, обратная матрица
        self.size = size  # размер ячеек

        # масштабирование матрицы поворота
        self.orientation.a00 *= size
        self.orientation.a01 *= size
        self.orientation.a10 *= size
        self.orientation.a11 *= size

    def translate(self, pos):
        """Переместить систему координат вдоль осей x и y"""
        dx, dy = pos

        self.orientation.a02 += dx * CAMERA_SPEED
        self.orientation.a12 += dy * CAMERA_SPEED

    def rotate(self, angle):
        """Повернуть систему координат на указанный угол"""
        angle_rad = math.radians(angle) * ROTATION_SPEED
        sin = math.sin(angle_rad)
        cos = math.cos(angle_rad)

        self.orientation.a00 = cos * self.orientation.a00 + sin * self.orientation.a10
        self.orientation.a01 = cos * self.orientation.a01 + sin * self.orientation.a11
        self.orientation.a02 = cos * self.orientation.a02 + sin * self.orientation.a12
        self.orientation.a10 = cos * self.orientation.a10 - sin * self.orientation.a00
        self.orientation.a11 = cos * self.orientation.a11 - sin * self.orientation.a01
        self.orientation.a12 = cos * self.orientation.a12 - sin * self.orientation.a02
        self.orientation.angle += angle

    def scale(self, scale):
        """Отмасштабировать систему координат на указанное значение"""
        self.orientation.a00 *= scale
        self.orientation.a01 *= scale
        self.orientation.a02 *= scale
        self.orientation.a10 *= scale
        self.orientation.a11 *= scale
        self.orientation.a12 *= scale
        self.size *= scale

    def set_layout(self, orientation: Orientation, size):
        """Задание новой системы координат"""
        self.__init__(orientation, size)

    def print(self):
        print(self.orientation.a00, self.orientation.a01, self.orientation.a02,
              self.orientation.a10, self.orientation.a11, self.orientation.a12)


# применяемая система координат (перемещение, масштабирование, начальное положение)
LAYOUT = Layout(layout_flat, HEXAGON_SIZE)

# Преобразования систем координат
def hex_to_pixel(layout: Layout, hexagon: Hex):
    """Переводит из шестиугольной (Hexagonal) системы координат в экранную (2D) систему координат """
    M = layout.orientation  # матрицы поворота

    # перемножение матриц
    x = M.a00*hexagon.q + M.a01*hexagon.r + M.a02
    y = M.a10*hexagon.q + M.a11*hexagon.r + M.a12

    return Point(x + ORIGIN.x, y + ORIGIN.y)

def pixel_to_hex(layout: Layout, p: Point):
    """Переводит из экранной (2D) системы координат в шестиугольную (Hexagonal) систему координат"""
    b00, b01, b02, b10, b11, b12 = layout.orientation.reverse()  # матрицы поворота

    # перемножение матриц
    pt = Point(p.x - ORIGIN.x, p.y - ORIGIN.y)
    q = b00*pt.x + b01*pt.y + b02
    r = b10*pt.x + b11*pt.y + b12

    return Hex(q, r)

class Cell:
    """Класс Cell, содержащий всю информацию об ячейке шестиугольника"""
    def __init__(self, coordinate, color=None):
        #pygame.sprite.Sprite.__init__(self)
        self.corners = None  # положение вершин шестиугольника
        self.coordinate = coordinate  # координата ячейки
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color

    def draw(self, position, layout: Layout, selected=False):
        """Отрисовка шестиугольника на экране"""
        self.pixels_corners(position, layout)  # определение положения вершин шестиугольника

        # изменение отображения клетки при наведении на нее
        if selected:
            pygame.draw.polygon(screen, 0, self.corners)
        else:
            pygame.draw.polygon(screen, self.color, self.corners)
            pygame.draw.aalines(screen, 0, False, self.corners[:4])

    def pixels_corners(self, position, layout):
        """Возвращает список координат вершин треугольника"""
        self.corners = []  # положение вершин шестиугольника
        size, angle = layout.size, layout.orientation.angle
        x, y = position

        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.radians(angle_deg)
            self.corners.append((x + size * math.cos(angle_rad - math.radians(angle)),
                                 y + size * math.sin(angle_rad - math.radians(angle))))

        return self.corners

#cells = pygame.sprite.Group()

def check_events():
    """Управление"""
    global running
    global left_pressed
    global right_pressed
    global up_pressed
    global down_pressed
    global turn_counterclockwise
    global turn_clockwise

    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            running = False

        # нажатие клавиши
        if event.type == pygame.KEYDOWN:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = True
            if event.key == pygame.K_q:
                turn_counterclockwise = True
            if event.key == pygame.K_e:
                turn_clockwise = True

            # возвращение на начальную клетку
            if event.key == pygame.K_h:
                LAYOUT.set_layout(layout_flat, HEXAGON_SIZE)

        # отжатие клавиши
        if event.type == pygame.KEYUP:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = False
            if event.key == pygame.K_q:
                turn_counterclockwise = False
            if event.key == pygame.K_e:
                turn_clockwise = False

        # вращение колесика мыши
        if event.type == pygame.MOUSEWHEEL:
            # приближение/отдаление камеры
            LAYOUT.scale(1 + event.y * SCALE_SPEED)


    # УПРАВЛЕНИЕ КАМЕРОЙ
    # перемещение
    if left_pressed and not right_pressed:
        LAYOUT.translate((1, 0))
    if right_pressed and not left_pressed:
        LAYOUT.translate((-1, 0))
    if up_pressed and not down_pressed:
        LAYOUT.translate((0, 1))
    if down_pressed and not up_pressed:
        LAYOUT.translate((0, -1))
    # вращение
    if turn_clockwise and not turn_counterclockwise:
        LAYOUT.rotate(-1)
    if turn_counterclockwise and not turn_clockwise:
        LAYOUT.rotate(1)

# Функции, связанные с отображением объектов на экране
def intersect_dict_and_set(d: dict, s: set):
    """Возвращает часть словаря, с указанными ключами"""
    return {key: d[key] for key in set(d) & s}

def grid_border(coordinates: dict):
    """Возвращает координаты ячеек, находящиеся на экране"""
    radius = round(max(WIDTH//2 - BORDER, HEIGHT//2 - BORDER) / (sqrt3 * LAYOUT.size) + 2.5)  # радиус генерируемой сетки
    center = hex_round(pixel_to_hex(LAYOUT, ORIGIN))  # позиция ячейки в центре экрана
    screen_coord = {}

    # генерация сетки в центре экрана
    for q in range(-radius, radius + 1):
        for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
            hex_pos = Hex(q + center.q, r + center.r)
            if hex_pos in coordinates:
                screen_coord[hex_pos] = coordinates[hex_pos]

    #print(f"Размер словаря - {len(screen_coord)} объектов")
    return screen_coord

def draw_grid(coordinates):
    """Отрисовка ячеек на экране"""
    show_coord = True  # отображать координаты шестиугольников

    # положение курсора
    mouse_pixel_pos = Point(*pygame.mouse.get_pos())
    mouse_hex_pos = hex_round(pixel_to_hex(LAYOUT, mouse_pixel_pos))

    # ОТРИСОВКА ЯЧЕЕК
    for coordinate, hexagon in grid_border(coordinates).items():
        position = hex_to_pixel(LAYOUT, hexagon.coordinate)  # положение на экране
        # отображение объектов только в пределах экрана
        if (BORDER - sqrt3*LAYOUT.size < position.y < HEIGHT - BORDER + sqrt3*LAYOUT.size
                and BORDER - sqrt3*LAYOUT.size < position.x < WIDTH - BORDER + sqrt3*LAYOUT.size):
            if hexagon.coordinate == mouse_hex_pos:
                #cells.add(hexagon)
                hexagon.draw(position, LAYOUT, selected=True)
            else:
                hexagon.draw(position, LAYOUT)
            # отображение координат шестиугольников
            if show_coord:
                coord_text = font.render("{}, {}".format(*coordinate), False, WHITE)
                coord_text_rect = coord_text.get_rect()
                coord_text_rect.center = position
                screen.blit(coord_text, coord_text_rect)

    # ось q
    pygame.draw.line(screen, (255, 0, 0), hex_to_pixel(LAYOUT, Hex(0, 0)), hex_to_pixel(LAYOUT, Hex(1, 0)))
    # ось r
    pygame.draw.line(screen, (0, 255, 0), hex_to_pixel(LAYOUT, Hex(0, 0)), hex_to_pixel(LAYOUT, Hex(0, 1)))
    # границы экрана
    pygame.draw.rect(screen, 0, (BORDER, BORDER, WIDTH-2*BORDER, HEIGHT-2*BORDER), 3)

# Генерация поля
def generate_square_grid(width: int, height: int, center: Hex = None):
    """Генерация прямоугольной сетки"""
    coordinates = {}
    grid_height = height - 1

    # определение центра сетки
    if center is None:
        center = Hex(width // 2, grid_height // 2)

    # генерация сетки
    offset = 0
    for col in range(width, 0, -1):
        for row in range(int(offset)-1, int(offset) + grid_height):
            hex_pos = Hex(col - center.q - 1, row - center.r - 1)
            coordinates[hex_pos] = Cell(hex_pos)
        offset += .5

    return coordinates

def generate_hexagons_grid(radius: int, center: Hex = None):
    """Генерация сетки в форме шестиугольника"""
    coordinates = {}

    # определение центра сетки
    if center is None:
        center = Hex(0, 0)

    # генерация сетки
    for q in range(-radius, radius+1):
        for r in range(max(-radius, -q-radius), min(radius, -q+radius)+1):
            hex_pos = Hex(q + center.q, r + center.r)
            coordinates[hex_pos] = Cell(hex_pos)

    return coordinates

def update_screen():
    """Отобразит объекты на экране в определенном порядке"""
    screen.fill(BACKGROUND)
    #screen.blit(layer_hex, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    #screen.blit(layer_lines, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
    #cells.draw(screen)
    pygame.display.update()

def main():
    # координаты существующих шестиугольников
    coordinates = {Hex(0, 0): Cell(Hex(0, 0)),
                   Hex(1, 0): Cell(Hex(1, 0)),
                   Hex(0, 1): Cell(Hex(0, 1)),
                   Hex(1, 1): Cell(Hex(1, 1))}

    coordinates = generate_square_grid(60, 60)

    while running:
        clock.tick()

        check_events()  # управление и ивенты

        # ОТРИСОВКА И ОБНОВЛЕНИЕ ЭКРАНА

        screen.fill(BACKGROUND)
        draw_grid(coordinates)
        #update_screen()
        pygame.display.update()

        print("FPS:", clock.get_fps())
        #LAYOUT.print()

    pygame.quit()


if __name__ == "__main__":
    main()
