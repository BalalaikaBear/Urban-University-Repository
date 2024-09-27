class Screen:
    """Хранит информацию об экране приложения"""
    def __init__(self, width: int = 1600, height: int = 900) -> None:
        # размер экрана
        self.width = width
        self.height = height
        self.border = 150
        self.origin: tuple[int, int] = self.width // 2, self.height // 2


class Camera:
    """Скорость управления камерой"""
    def __init__(self, movement: float = 12, rotation: float = 1, scale: float = 1/20) -> None:
        self.movement = movement
        self.rotation = rotation
        self.scale = scale


class Settings:
    """Настройки игрока"""
    def __init__(self, screen: Screen = Screen, camera: Camera = Camera) -> None:
        self.screen = screen
        self.camera = camera


class Player:
    """Информация пользователя"""
    def __init__(self, name: str, settings: Settings = Settings) -> None:
        self.name = name
        self.id = hash(self.name)
        self.settings = settings

    def __str__(self) -> str:
        return f'{self.name} (ID: {self.id})'


# проверка нажатия кнопок
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
turn_counterclockwise = False
turn_clockwise = False