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
HEXAGON_SIZE = 50
FPS = 60
running = True

#
CAMERA_SPEED = 12
ROTATION_SPEED = 1

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
    def __init__(self, matrix: np, angle):
        # матрица поворота
        self.matrix = matrix

        # обратная матрица поворота
        self._reverse = inv(matrix)

        # начальный угол поворота ячеек
        self.angle = angle

    @property
    def reverse(self):
        self._reverse = inv(self.matrix)
        return self._reverse

    @reverse.setter
    def reverse(self, value: np):
        self._reverse = value


# стартовая ориентация ячеек
layout_flat = Orientation(np.array([[3/2, 0, 0],
                                   [math.sqrt(3)/2, math.sqrt(3), 0],
                                   [0, 0, 1]]),
                          0)

class Layout:
    """Система координат"""
    def __init__(self, start_orientation: Orientation, size):
        self.orientation = copy.deepcopy(start_orientation)  # матрица поворота, обратная матрица
        self.size = size  # размер ячеек

        # масштабирование матрицы поворота
        self.orientation.matrix *= size
        self.orientation.matrix[2, 2] = 1

    def translate(self, pos):
        """Переместить систему координат вдоль осей x и y"""
        dx, dy = pos
        translate_matrix = np.array([[1, 0, dx * CAMERA_SPEED],
                                     [0, 1, dy * CAMERA_SPEED],
                                     [0, 0, 1]])
        self.orientation.matrix = translate_matrix @ self.orientation.matrix

    def rotate(self, angle):
        """Повернуть систему координат на указанный угол"""
        angle_rad = math.radians(angle) * ROTATION_SPEED
        rotation_matrix = np.array([[math.cos(angle_rad), math.sin(angle_rad), 0],
                                    [-math.sin(angle_rad), math.cos(angle_rad), 0],
                                    [0, 0, 1]])
        self.orientation.matrix = rotation_matrix @ self.orientation.matrix
        self.orientation.angle += angle

    def scale(self, scale):
        """Отмасштабировать систему координат на указанное значение"""
        scaling_matrix = np.array([[scale, 0, 0],
                                  [0, scale, 0],
                                  [0, 0, 1]])
        self.size *= scale
        self.orientation.matrix = scaling_matrix @ self.orientation.matrix

    def set_layout(self, orientation: Orientation, size):
        """Задание новой системы координат"""
        self.__init__(orientation, size)

    def print(self):
        print(self.orientation.matrix)


# применяемая система координат (перемещение, масштабирование, начальное положение)
LAYOUT = Layout(layout_flat, HEXAGON_SIZE)

# Преобразования систем координат
def hex_to_pixel(layout: Layout, hexagon: Hex):
    """Переводит из шестиугольной (Hexagonal) системы координат в экранную (2D) систему координат """
    matrix = layout.orientation.matrix  # матрицы поворота
    origin = Point(WIDTH // 2, HEIGHT // 2)  # начало координат

    # перемножение матриц
    hexagon = np.array([hexagon.q, hexagon.r, 1])
    pixel = matrix @ hexagon  # [x, y, 1]

    return Point(pixel[0] + origin.x, pixel[1] + origin.y)

def pixel_to_hex(layout: Layout, p: Point):
    """Переводит из экранной (2D) системы координат в шестиугольную (Hexagonal) систему координат"""
    rev_matrix = layout.orientation.reverse  # матрицы поворота
    origin = Point(WIDTH // 2, HEIGHT // 2)  # начало координат

    # перемножение матриц
    pt = np.array([[p.x - origin.x], [p.y - origin.y], [1]])
    hex_pos = rev_matrix @ pt  # [q, r, 1]

    return Hex(hex_pos[0, 0], hex_pos[1, 0])

class Cell:
    """Класс Cell, содержащий всю информацию об ячейке шестиугольника"""
    def __init__(self, coordinate, color=None):
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
    screen_hex = set()  # положение всех ячеек на экране
    radius = round(max(WIDTH//2 - BORDER, HEIGHT//2 - BORDER) / (math.sqrt(3) * LAYOUT.size) + 2.5)  # радиус генерируемой сетки
    center = hex_round(pixel_to_hex(LAYOUT, Point(WIDTH // 2, HEIGHT // 2)))  # позиция ячейки в центре экрана

    # генерация сетки в центре экрана
    for q in range(-radius, radius + 1):
        for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
            hex_pos = Hex(q + center.q, r + center.r)
            screen_hex.add(hex_pos)

    return intersect_dict_and_set(coordinates, screen_hex)

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
        if (BORDER - math.sqrt(3)*LAYOUT.size < position.y < HEIGHT - BORDER + math.sqrt(3)*LAYOUT.size
                and BORDER - math.sqrt(3)*LAYOUT.size < position.x < WIDTH - BORDER + math.sqrt(3)*LAYOUT.size):
            if hexagon.coordinate == mouse_hex_pos:
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
    pygame.display.update()

def main():
    # координаты существующих шестиугольников
    coordinates = {Hex(0, 0): Cell(Hex(0, 0)),
                   Hex(1, 0): Cell(Hex(1, 0)),
                   Hex(0, 1): Cell(Hex(0, 1)),
                   Hex(1, 1): Cell(Hex(1, 1))}

    coordinates = generate_square_grid(60, 60)

    while running:
        clock.tick(FPS)

        check_events()  # управление и ивенты

        # ОТРИСОВКА И ОБНОВЛЕНИЕ ЭКРАНА

        screen.fill(BACKGROUND)
        draw_grid(coordinates)
        #update_screen()
        pygame.display.update()

        #print(clock.get_fps())
        #LAYOUT.print()

    pygame.quit()


if __name__ == "__main__":
    main()
