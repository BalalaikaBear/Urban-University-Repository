import pygame
from typing import Optional

class Screen:
    """Хранит информацию об экране приложения"""
    def __init__(self, width: int = 1600, height: int = 900) -> None:
        # размер экрана
        self.width = width
        self.height = height
        self.border: int = 150
        self.origin: tuple[int, int] = (self.width // 2, self.height // 2)
        self.py_screen: pygame.Surface | pygame.SurfaceType = pygame.display.set_mode((self.width, self.height))


class Camera:
    """Скорость управления камерой"""
    def __init__(self, movement: float = 12, rotation: float = 1, scale: float = 1/20) -> None:
        self.movement = movement
        self.rotation = rotation
        self.scale = scale

class Inputs:
    """Хранит информацию о нажатых клавишах"""
    def __init__(self):
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.turn_counterclockwise = False
        self.turn_clockwise = False


class Settings:
    """Настройки игрока"""
    def __init__(self,
                 screen: Optional[Screen] = None,
                 camera: Optional[Camera] = None,
                 inputs: Optional[Inputs] = None,
                 *,
                 fps: int = 60) -> None:
        if screen is None:
            self.screen = Screen()
        else:
            self.screen = screen
        if camera is None:
            self.camera = Camera()
        else:
            self.camera = camera
        if inputs is None:
            self.inputs = Inputs()
        else:
            self.inputs = inputs
        self.fps = fps
        self.running = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.font: pygame.font = pygame.font.SysFont("Arial", 14)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    settings = Settings()
    print(settings.screen.origin)
