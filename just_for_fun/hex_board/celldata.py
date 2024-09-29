import random, math, numpy, pygame
from layout import Layout

# Сокращение записи типов объектов
type Hex[q, r] = tuple[float | numpy.ndarray, float | numpy.ndarray]
type Point[x, y] = tuple[float | numpy.ndarray, float | numpy.ndarray]


class Cell:
    """Класс Cell, содержащий всю информацию об ячейке шестиугольника"""
    def __init__(self, coordinate: Hex, color=None) -> None:
        self.corners = None  # положение вершин шестиугольника
        self.coordinate = coordinate  # координата ячейки [q, r]
        if color is None:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        else:
            self.color = color

    def draw(self,
             position: Point,
             layout: Layout,
             screen: pygame.Surface | pygame.SurfaceType,
             selected=False) -> None:
        """
        Отрисовка шестиугольника на экране

        :param position: Положение центра шестиугольника в координатах [x, y]
        :param layout: Система координат
        :param screen: Экран отображения
        :param selected: Выделена ли данная ячейка (изменяет отображение ячейки)
        :return:
        """
        self.pixels_corners(position, layout)  # определение положения вершин шестиугольника

        # изменение отображения клетки при наведении на нее
        if selected:
            pygame.draw.polygon(screen, 0, self.corners)
        else:
            pygame.draw.polygon(screen, self.color, self.corners)
            pygame.draw.aalines(screen, 0, False, self.corners[:4])

    def pixels_corners(self, position: Point, layout: Layout) -> list[Point]:
        """
        Возвращает список координат вершин треугольника

        :param position: Положение центра шестиугольника в координатах [x, y]
        :param layout: Система координат
        :return:
        """
        self.corners: list = []  # положение вершин шестиугольника
        for i in range(6):
            angle_deg: float = 60 * i
            angle_rad: float = math.radians(angle_deg)
            self.corners.append(
                (position[0] + layout.orientation.size * math.cos(angle_rad - math.radians(layout.orientation.angle)),
                 position[1] + layout.orientation.size * math.sin(angle_rad - math.radians(layout.orientation.angle))))
        return self.corners
