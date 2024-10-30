import pygame

from just_for_fun.voronoi_grid_2.interface.styleclass import Style

class Window:
    """Окно, отображаемое на экране"""
    def __init__(self,
                 screen: pygame.Surface,
                 anchor: tuple[int, int] | str,
                 objects: list[list],
                 auto_resize: bool = False,
                 style: type[Style] = Style) -> None:
        self._screen = screen
        self._anchor = anchor
        self._objects = objects
        self._auto_resize = auto_resize
        self.style = style(self._screen,
                           self._anchor,
                           self._objects,
                           self._auto_resize)

    def draw(self) -> None:
        """Рисование окна на экране"""
        self.style.draw()


if __name__ == '__main__':
    WIDTH = 1600
    HEIGHT = 1200
    running = True

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()

    window = Window(screen, 'left', [])
    window.draw()

    # игровой цикл
    while running:
        for event in pygame.event.get():
            # закрытие игры
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()