from typing import Any, Callable
import threading
import pygame

from just_for_fun.voronoi_grid_2.interface.constants.anchors import Anchor
from just_for_fun.voronoi_grid_2.interface.windows import Window
from just_for_fun.voronoi_grid_2.interface.styleclass import Style
from just_for_fun.voronoi_grid_2.interface.ui_elements import *

class Interface:
    def __init__(self, screen: pygame.Surface, windows: list[Window] = None):
        if windows is None:
            self.windows: dict[int | str, list[Window]] = {'main': []}  # {<номер слоя>: list[Window, ...]}
        else:
            self.windows = {}
            self.windows['main'] = windows

        self.screen: pygame.Surface = screen
        self.interface_screen: pygame.Surface = pygame.Surface(self.screen.size).convert_alpha()

        self.timer: threading.Timer | None = None
        self.previous_value: Any = None

    def draw(self) -> None:
        """Отрисовка интерфейса"""
        for layer, windows in self.windows.items():
            for window in windows:
                window.draw()
                self.pointed(window)

    def click(self) -> None:
        """Нажатие на кнопку в окне"""
        for layer, windows in self.windows.items():
            for window in windows:
                if window.inside(pygame.mouse.get_pos()):
                    window.click()

    def pointed(self, window: Window) -> None:
        """Определение наведения на окно"""
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        current_value: tuple[int, int] = mouse_pos[0] // 5, mouse_pos[1] // 5
        if window.inside(mouse_pos):
            if current_value != self.previous_value:
                if self.timer is not None:
                    self.timer.cancel()
                self.timer: threading.Timer = threading.Timer(2, window.pointed)
                self.timer.start()
            self.previous_value = current_value
        else:
            if current_value != self.previous_value and self.timer is not None:
                self.timer.cancel()

    def force_pointed(self) -> None:
        """Показывает справочное окно при нажатии"""
        if self.timer is not None:
            self.timer.cancel()

    @staticmethod
    def _wrapped_function(func) -> Callable:
        """Обертка, для сохранения ссылки на функцию"""
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper._func = func
        return wrapper


if __name__ == '__main__':
    WIDTH = 1600
    HEIGHT = 1200
    BACKGROUND: pygame.Color = pygame.color.Color(200, 200, 200)
    running = True

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()

    window_mouse = Window(screen, Anchor.MOUSE,
                    objects=[
                        [Icon('img.png'), Text('Icon')],
                        [Text('This is'), IconText('iron', 'iron.png')],
                        [Text('End of line')]
                    ])

    window_left_menu = Window(screen, Anchor.TOP_LEFT,
                              objects=[
                                  [Icon('menu.png')]
                              ])

    GUI = Interface(screen, [window_mouse, window_left_menu])

    # игровой цикл
    while running:
        for event in pygame.event.get():
            # закрытие игры
            if event.type == pygame.QUIT:
                running = False

            # нажатие ЛКМ
            if event.type == pygame.MOUSEBUTTONDOWN:
                GUI.click()

            if event.type == pygame.KEYDOWN:
                # ускорение отображения подсказки
                if event.key == pygame.K_q:
                    GUI.force_pointed()

        screen.fill(BACKGROUND)

        GUI.draw()

        pygame.display.update()
    pygame.quit()