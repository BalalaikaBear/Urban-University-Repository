from pprint import pprint
from typing import Any
import pygame

from just_for_fun.voronoi_grid_2.interface.constants.anchors import Anchor
from just_for_fun.voronoi_grid_2.interface.ui_elements import *

class Style:
    """Визуальный стиль окна"""
    def __init__(self,
                 screen: pygame.Surface,
                 anchor: tuple[int, int] | Anchor,
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

        # окно
        self.canvas_radius: int = 10
        self.canvas_spacing: int = 10
        self.canvas_color: pygame.Color = pygame.color.Color('#F3F2EE')
        self.shadow_size: int = 20
        self.shadow_color: pygame.Color = pygame.color.Color('#BBBBBB')

        # курсор
        self.cursor_size: tuple[int, int] = 20, 20
        self.border: int = 30

        # размеры слайдера
        self.slider_width: int = 100
        self.slider_height: int = 36

        self._calculate_window_size(objects)

    def _calculate_window_size(self, objects) -> None:
        """Определение размеров объектов и их расположение в окне"""
        self.objects: list[list[Any, tuple[int, int]]] = []
        self.window_width: int = self.canvas_spacing
        self.window_height: int = int(self.canvas_spacing - 0.1 * self.size)

        for line_index, line in enumerate(objects):
            line_height: int = 0
            line_width: int = self.canvas_spacing
            self.objects.append([])

            for item in line:
                # масштабирование размера
                if hasattr(item, 'size'):
                    size = round(item.size * self.size, 0) if item.size else self.size
                else:
                    size = self.size
                # добавление координат к объекту
                self.objects[line_index].append([item, (line_width, self.window_height), size])

                # иконка с текстом
                if isinstance(item, IconText):
                    font: pygame.font.Font = pygame.font.SysFont(item.front, size)
                    x, y = font.size(item.text)

                    # габариты объекта
                    line_width += x + size + self.icon_right_spacing
                    if y2 := max(y, size) > line_height:
                        line_height = y2

                # текст
                elif isinstance(item, Text):
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
                self.window_width = line_width + self.canvas_spacing
            self.window_height += line_height + self.line_spacing
        self.window_height += self.canvas_spacing

    def draw_pos(self) -> tuple[int, int]:
        """Определение координаты отрисовки окна"""
        if self.anchor == Anchor.MOUSE:
            mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
            screen_size: tuple[int, int] = self.screen.get_size()

            # по оси X
            if mouse_pos[0] > screen_size[0] - self.window_width - self.cursor_size[0] - self.border:
                wx: int = min(mouse_pos[0] - self.window_width,
                              screen_size[0] - self.border - self.window_width)
                # по оси Y
                if mouse_pos[1] > screen_size[1] - self.window_height - self.cursor_size[1] - self.border:  # лево верх
                    wy: int = min(mouse_pos[1] - self.window_height,
                                  screen_size[1] - self.border - self.window_height)
                else:  # лево низ
                    wy: int = max(mouse_pos[1],
                                  self.border)
            else:
                wx: int = max(mouse_pos[0] + self.cursor_size[0], self.border)
                # по оси Y
                if mouse_pos[1] > screen_size[1] - self.window_height - self.cursor_size[1] - self.border:  # право верх
                    wx: int = max(mouse_pos[0],
                                  self.border)
                    wy: int = min(mouse_pos[1] - self.window_height,
                                  screen_size[1] - self.border - self.window_height)
                else:  # право низ (стандартное положение)
                    wy: int = max(mouse_pos[1] + self.cursor_size[1],
                                  self.border)
            return wx, wy

        elif self.anchor == Anchor.TOP_LEFT:
            return self.border, self.border

    def draw(self) -> None:
        """Рисование окна на экране"""
        # определение координаты отрисовки окна
        window_coord: tuple[int, int] = self.draw_pos()

        # рисование окна
        self.draw_rect_with_shadow(window_coord)

        # рисование объектов в окне
        for line in self.objects:
            for item, coordinate, size in line:
                # координата отрисовки объектов
                coordinate: tuple[int, int] = (coordinate[0] + window_coord[0],
                                               coordinate[1] + window_coord[1])

                # иконка с текстом
                if isinstance(item, IconText):
                    continue

                # текст
                elif isinstance(item, Text):
                    text_surface: pygame.Surface = pygame.font.SysFont(item.front, size).render(
                        item.text, True, self.front_color)
                    self.screen.blit(text_surface, coordinate)

                # иконка
                elif isinstance(item, Icon):
                    continue

                # окно флажка
                elif isinstance(item, CheckBox):
                    continue

                # слайдер
                elif isinstance(item, Slider):
                    continue

    def draw_rect_with_shadow(self, window_coord: tuple[int, int]) -> None:
        # поверхность, на которой рисуется окно
        shadow_surface: pygame.Surface = pygame.Surface((self.window_width + 2*self.shadow_size,
                                                         self.window_height + 2*self.shadow_size)).convert_alpha()
        shadow_surface.fill((255, 255, 255, 0))
        # рисование тени
        pygame.draw.rect(shadow_surface,
                         self.shadow_color,
                         (self.shadow_size, self.shadow_size, self.window_width, self.window_height),
                         border_radius=self.canvas_radius)

        # размытие тени
        shadow_surface = pygame.transform.gaussian_blur(shadow_surface, self.shadow_size // 2)
        # рисование окна
        pygame.draw.rect(shadow_surface,
                         self.canvas_color,
                         (self.shadow_size, self.shadow_size, self.window_width, self.window_height),
                         border_radius=self.canvas_radius)
        # рисование окна на основном экране
        self.screen.blit(shadow_surface, (window_coord[0] - self.shadow_size, window_coord[1] - self.shadow_size))
