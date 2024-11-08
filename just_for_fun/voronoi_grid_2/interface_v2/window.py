from just_for_fun.voronoi_grid_2.interface_v2.ui_elements import Container
from just_for_fun.voronoi_grid_2.interface_v2.constants.anchors import Anchor
import pygame

class Window:
    def __init__(self,
                 container: Container,
                 anchor: Anchor = Anchor.CENTER,
                 *,
                 resizable: bool = False,
                 movable: bool = False) -> None:
        self.container = container
        self.anchor = anchor
        self.resizable = resizable
        self.movable = movable
        self.rect: pygame.Rect = self.container.size_of_container()

        # список всех контейнеров в окне
        self.widgets: list[Container] = []
        self._make_widgets_list(self.container)

    def _make_widgets_list(self, container: Container) -> None:
        """Заполняет список всех контейнеров/виджетов в окне"""
        if hasattr(container, 'children') and container.children:
            for child in container.children:
                self.widgets.append(child)      # добавить контейнер/виджет в общий список
                self._make_widgets_list(child)  # и входящие в него контейнеры также добавить в общий список
