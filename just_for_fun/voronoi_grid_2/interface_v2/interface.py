from just_for_fun.voronoi_grid_2.interface_v2.window import Window
from just_for_fun.voronoi_grid_2.interface_v2.ui_elements import *
from typing import Any, Callable
import threading
import pygame

class Interface:
    def __init__(self, screen: pygame.Surface, windows: list[Window], *, debug_mode: bool = False):
        self.final_screen = screen  # поверхность, на которую будет выводиться интерфейс
        self.ui_screen: pygame.Surface = pygame.Surface(self.final_screen.size).convert_alpha()  # поверхность с отрисованным интерфейсом
        self.windows = windows  # список всех окон на экране

        # режим отладки (отображение краев контейнеров)
        self.debug_mode = debug_mode

        # таймер, отображающий всплывающую подсказку
        self.timer: threading.Timer | None = None
        self.previous_value: Any = None

    def mouse_detect(self) -> Container | None:
        """Возвращает контейнер/виджет, работающий при наведении на него, если он находится под курсором"""
        if self.debug_mode:
            self.widgets_under_mouse: list[tuple[Window, Container]] = []
            flag: bool = True

        for window in self.windows[::-1]:
            # определение окна по позиции мыши
            if window.rect.collidepoint(pygame.mouse.get_pos()):
                for widget in window.widgets[::-1]:
                    # определение контейнера/виджета по позиции мыши
                    if widget.min_size.collidepoint(pygame.mouse.get_pos()):

                        if self.debug_mode:
                            self.widgets_under_mouse.append((window, widget))
                            if widget.touchable and flag:
                                touchable_widget: Container = widget
                                flag = False

                        # если виджет реагирует на мышь -> вернуть виджет
                        elif widget.touchable:
                            return widget

        if self.debug_mode:
            return touchable_widget

    def click(self) -> None:
        """Вызывает выполнение кнопки (контейнера/виджета) при нажатии"""
        widget: Container | None = self.mouse_detect()
        if widget and hasattr(widget, 'click'):
            widget.click()

    def pointed(self) -> None:
        """Вызов окна подсказки по истечению n секунд"""
        mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
        current_value: tuple[int, int] = mouse_pos[0] // 5, mouse_pos[1] // 5

        # таймер по сравнению предыдущего положения мыши,
        # при несоответствии значений -> запускать таймер заново
        if current_value != self.previous_value:
            if self.timer is not None:
                self.timer.cancel()
            self.timer: threading.Timer = threading.Timer(2, lambda: True)
            self.timer.start()
        self.previous_value = current_value

        # по истечению таймера вызвать окно подсказки (если оно прописано)
        if not self.timer.isAlive():
            widget: Container | None = self.mouse_detect()
            if widget and hasattr(widget, 'pointed'):
                widget.pointed()

    def draw(self) -> None:
        self.ui_screen.fill((0, 0, 0, 0))  # окраска экрана интерфейса

        # отрисовка окон
        for window in self.windows:
            pygame.draw.rect(self.ui_screen, '#99D9EA', window.rect, 1)

        self.final_screen.blit(self.ui_screen, (0, 0))  # проецирование интерфейса на экран

if __name__ == '__main__':
    WIDTH = 1600
    HEIGHT = 1200
    BACKGROUND: pygame.Color = pygame.color.Color(200, 200, 200)
    running = True

    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock: pygame.time.Clock = pygame.time.Clock()

    window_left_menu = Window(Container(TextBox('This is a TestBox message'), max_size=(400, 1000)))
    print(window_left_menu.widgets)

    GUI = Interface(screen, [window_left_menu], debug_mode=True)

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
                    #GUI.force_pointed()
                    pass

        screen.fill(BACKGROUND)

        GUI.draw()

        pygame.display.update()
    pygame.quit()