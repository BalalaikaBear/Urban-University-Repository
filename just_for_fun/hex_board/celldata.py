import random, math
from numbers import Real  # real numbers as a type
from coordinates import Layout
from gameinit import *

# Сокращение записи типов объектов
type Hex[q, r] = tuple[Real, Real]
type Point[x, y] = tuple[Real, Real]

screen = pygame.display.set_mode((settings.screen.width, settings.screen.height))


class Cell:
    """Класс Cell, содержащий всю информацию об ячейке шестиугольника"""

    def __init__(self, coordinate: Hex, color=None) -> None:
        self.corners = None  # положение вершин шестиугольника
        self.coordinate = coordinate  # координата ячейки
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color

    def draw(self, position: Point, layout: Layout, selected=False) -> None:
        """Отрисовка шестиугольника на экране"""
        self.pixels_corners(position, layout)  # определение положения вершин шестиугольника

        # изменение отображения клетки при наведении на нее
        if selected:
            pygame.draw.polygon(screen, 0, self.corners)
        else:
            pygame.draw.polygon(screen, self.color, self.corners)
            pygame.draw.aalines(screen, 0, False, self.corners[:4])

    def pixels_corners(self, position: Point, layout: Layout) -> list[Point]:
        """Возвращает список координат вершин треугольника"""
        self.corners: list = []  # положение вершин шестиугольника
        for i in range(6):
            angle_deg: Real = 60 * i
            angle_rad: Real = math.radians(angle_deg)
            self.corners.append(
                (position[0] + layout.orientation.size * math.cos(angle_rad - math.radians(layout.orientation.angle)),
                 position[1] + layout.orientation.size * math.sin(angle_rad - math.radians(layout.orientation.angle))))
        return self.corners
