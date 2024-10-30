import pygame

from just_for_fun.voronoi_grid_2.interface.ui_elements import *

class Style:
    """Визуальный стиль окна"""
    def __init__(self,
                 screen: pygame.Surface,
                 anchor: tuple[int, int] | str,
                 objects: list[list],
                 auto_resize: bool = False) -> None:
        self.screen = screen
        self.anchor = anchor
        self.objects = objects
        self.auto_resize = auto_resize
        self.objects_pos: list[list] = []

    def draw(self) -> None:
        """Рисование окна на экране"""
        for line in self.objects:
            for item in line:
                # текст
                if isinstance(item, Text):
                    print(item.text)

                # иконка
                elif isinstance(item, Icon):
                    print(item.img)

                # иконка с текстом
                elif isinstance(item, IconText):
                    print(item.text, item.img)

                # окно флажка
                elif isinstance(item, CheckBox):
                    print(item.named_state)

                # слайдер
                elif isinstance(item, Slider):
                    print(item.value)
