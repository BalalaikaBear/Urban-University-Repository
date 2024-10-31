from typing import Any
import pygame

from just_for_fun.voronoi_grid_2.interface.styleclass import Style
from just_for_fun.voronoi_grid_2.interface.ui_elements import *

class Window:
    """Окно, отображаемое на экране"""
    def __init__(self,
                 screen: pygame.Surface,
                 anchor: tuple[int, int] | str,
                 objects: list[list[Any]],
                 is_table: bool = False,
                 style: type[Style] = Style) -> None:
        self._screen = screen
        self._anchor = anchor
        self._objects = objects
        self._is_table = is_table
        self.style = style(self._screen,
                           self._anchor,
                           self._objects,
                           self._is_table)

    def draw(self) -> None:
        """Рисование окна на экране"""
        self.style.draw()


if __name__ == '__main__':
    WIDTH = 1600
    HEIGHT = 1200
    BACKGROUND: pygame.Color = pygame.color.Color(200, 200, 200)
    running = True

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()

    window = Window(screen, 'mouse',
                    objects=[
                        [Icon('img.png'), Text('Icon')],
                        [Text('This is'), IconText('iron', 'iron.png')],
                        [Text('End of line')]
                    ])

    # игровой цикл
    while running:
        for event in pygame.event.get():
            # закрытие игры
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND)

        window.draw()

        pygame.display.update()
    pygame.quit()