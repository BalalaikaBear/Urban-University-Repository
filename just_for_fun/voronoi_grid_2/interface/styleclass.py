from pprint import pprint
from typing import Any
import pygame

from just_for_fun.voronoi_grid_2.interface.ui_elements import *

class Style:
    """Визуальный стиль окна"""
    def __init__(self,
                 screen: pygame.Surface,
                 anchor: tuple[int, int] | str,
                 objects: list[list[Any]],
                 is_table: bool = False) -> None:
        self.screen = screen
        self.anchor = anchor
        self.is_table = is_table

        # шрифт
        self.front: str = 'Arial'
        self.front_color: pygame.Color = pygame.color.Color(0, 0, 0)
        self.size: int = 20
        self.line_spacing: int = 0
        self.icon_right_spacing: int = 4

        # курсор
        self.cursor_size: tuple[int, int] = 20, 20

        # размеры слайдера
        self.slider_width: int = 100
        self.slider_height: int = 36

        self._calculate_window_size(objects)

    def _calculate_window_size(self, objects) -> None:
        """Определение размеров объектов и их расположение в окне"""
        self.objects: list[list[Any, tuple[int, int]]] = []
        self.window_width: int = 0
        self.window_height: int = 0

        for line_index, line in enumerate(objects):
            line_height: int = 0
            line_width: int = 0
            self.objects.append([])

            for item in line:
                # масштабирование размера
                if hasattr(item, 'size'):
                    size = round(item.size * self.size, 0) if item.size else self.size
                else:
                    size = self.size
                # добавление координат к объекту
                self.objects[line_index].append([item, (line_width, self.window_height), size])

                # текст
                if isinstance(item, Text):
                    font: pygame.font.Font = pygame.font.SysFont(item.front, size)
                    x, y = font.size(item.text + " ")

                    # габариты объекта
                    line_width += x
                    if y > line_height:
                        line_height = y

                # иконка
                elif isinstance(item, Icon):
                    # габариты объекта
                    line_width += size + self.icon_right_spacing
                    if size > line_height:
                        line_height = size

                # иконка с текстом
                elif isinstance(item, IconText):
                    font: pygame.font.Font = pygame.font.SysFont(item.front, size)
                    x, y = font.size(item.text)

                    # габариты объекта
                    line_width += x + size + self.icon_right_spacing
                    if y2 := max(y, size) > line_height:
                        line_height = y2

                # окно флажка
                elif isinstance(item, CheckBox):
                    # габариты объекта
                    line_width += size
                    if self.size > line_height:
                        line_height = self.size

                # слайдер
                elif isinstance(item, Slider):
                    # габариты объекта
                    line_width += self.slider_width
                    if self.slider_height > line_height:
                        line_height = self.slider_height

            if line_width > self.window_width:
                max_width = line_width
            self.window_height += line_height + self.line_spacing

    def draw(self) -> None:
        """Рисование окна на экране"""
        for line in self.objects:
            for item, coordinate, size in line:
                # координата отрисовки объектов
                if self.anchor == 'mouse':
                    mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
                    coordinate: tuple[int, int] = (coordinate[0] + self.cursor_size[0] + mouse_pos[0],
                                                   coordinate[1] + self.cursor_size[1] + mouse_pos[1])

                # иконка с текстом
                if isinstance(item, IconText):
                    print(item.text, item.img)

                # текст
                elif isinstance(item, Text):
                    text_surface: pygame.Surface = pygame.font.SysFont(item.front, size).render(
                        item.text, True, self.front_color)
                    self.screen.blit(text_surface, coordinate)

                # иконка
                elif isinstance(item, Icon):
                    print(item.img)

                # окно флажка
                elif isinstance(item, CheckBox):
                    print(item.named_state)

                # слайдер
                elif isinstance(item, Slider):
                    print(item.value)
