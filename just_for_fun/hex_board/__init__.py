import sys, math, numpy, pygame
import hexmath, mapgen
from layout import Layout, Orientation
from mapdata import Map
from celldata import Cell
from settings import Settings, Screen, Camera

# Сокращение записи типов объектов
type Hex[q, r] = tuple[float | numpy.ndarray, float | numpy.ndarray]
type Point[x, y] = tuple[float | numpy.ndarray, float | numpy.ndarray]

# Константы
sqrt3 = math.sqrt(3)

# инициализация
pygame.init()
pygame.font.init()
settings = Settings()

# скорость перемещения камеры
settings.camera.movement = 12
settings.camera.rotation = 1
settings.camera.scale = 1/20
print(settings.screen.origin)

# цвета
BACKGROUND = pygame.color.Color(200, 200, 200)
WHITE = pygame.color.Color(255, 255, 255)

# слои экрана
layer_hex = pygame.Surface((settings.screen.width, settings.screen.height))
layer_lines = pygame.Surface((settings.screen.width, settings.screen.height))
layer_text = pygame.Surface((settings.screen.width, settings.screen.height))

# стартовая ориентация ячеек
layout_flat = Orientation(numpy.array([[3/2, 0, 0],
                                       [sqrt3/2, sqrt3, 0],
                                       [0, 0, 1]]),
                          angle=0,
                          size=50)

# применяемая система координат (перемещение, масштабирование, начальное положение)
LAYOUT = Layout(layout_flat, settings=settings)

def check_events() -> None:
    """Управление"""
    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            settings.running = False

        # нажатие клавиши
        if event.type == pygame.KEYDOWN:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                settings.inputs.left_pressed = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                settings.inputs.right_pressed = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                settings.inputs.up_pressed = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                settings.inputs.down_pressed = True
            if event.key == pygame.K_q:
                settings.inputs.turn_counterclockwise = True
            if event.key == pygame.K_e:
                settings.inputs.turn_clockwise = True

            # возвращение на начальную клетку
            if event.key == pygame.K_h:
                LAYOUT.set_layout(layout_flat)

        # отжатие клавиши
        if event.type == pygame.KEYUP:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                settings.inputs.left_pressed = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                settings.inputs.right_pressed = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                settings.inputs.up_pressed = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                settings.inputs.down_pressed = False
            if event.key == pygame.K_q:
                settings.inputs.turn_counterclockwise = False
            if event.key == pygame.K_e:
                settings.inputs.turn_clockwise = False

        # вращение колесика мыши
        if event.type == pygame.MOUSEWHEEL:
            # приближение/отдаление камеры
            print(event.y)
            LAYOUT.scale(1 + event.y * settings.camera.scale)

    # УПРАВЛЕНИЕ КАМЕРОЙas
    # перемещение
    if settings.inputs.left_pressed and not settings.inputs.right_pressed:
        LAYOUT.translate((1, 0))
    if settings.inputs.right_pressed and not settings.inputs.left_pressed:
        LAYOUT.translate((-1, 0))
    if settings.inputs.up_pressed and not settings.inputs.down_pressed:
        LAYOUT.translate((0, 1))
    if settings.inputs.down_pressed and not settings.inputs.up_pressed:
        LAYOUT.translate((0, -1))
    # вращение
    if settings.inputs.turn_clockwise and not settings.inputs.turn_counterclockwise:
        LAYOUT.rotate(-1)
    if settings.inputs.turn_counterclockwise and not settings.inputs.turn_clockwise:
        LAYOUT.rotate(1)

def grid_border(coordinates: Map) -> dict:
    """Возвращает координаты ячеек, находящиеся на экране"""
    # радиус генерируемой сетки
    radius: int = round(max(settings.screen.width // 2 - settings.screen.border,
                            settings.screen.height // 2 - settings.screen.border) / (sqrt3 * LAYOUT.orientation.size) + 2.5)
    # позиция ячейки в центре экрана
    center: Hex = hexmath.round(hexmath.pixel_to_hex(LAYOUT, settings.screen.origin, settings=settings))
    screen_coord: dict = {}

    # генерация сетки в центре экрана
    for q in range(-radius, radius + 1):
        for r in range(max(-radius, -q - radius), min(radius, -q + radius) + 1):
            hex_pos: Hex = (q + center[0], r + center[1])
            if hex_pos in coordinates:
                screen_coord[hex_pos] = coordinates[hex_pos]

    #print(f"Размер словаря - {len(screen_coord)} объектов")
    return screen_coord

def draw_grid(coordinates: Map) -> None:
    """Отрисовка ячеек на экране"""
    show_coord = True  # отображать координаты шестиугольников

    # положение курсора
    mouse_pixel_pos: tuple[int, int] = pygame.mouse.get_pos()
    mouse_hex_pos = hexmath.round(hexmath.pixel_to_hex(LAYOUT, mouse_pixel_pos, settings=settings))

    # ОТРИСОВКА ЯЧЕЕК
    for coordinate, hexagon in grid_border(coordinates).items():
        position: Point = LAYOUT.get_pos(coordinate)  # положение на экране
        #wwaposition: Point = hexmath.hex_to_pixel(LAYOUT, hexagon.coordinate, settings=settings)  # положение на экране
        # отображение объектов только в пределах экрана
        if (settings.screen.border - sqrt3*LAYOUT.orientation.size < position[1] < settings.screen.height - settings.screen.border + sqrt3*LAYOUT.orientation.size
            and settings.screen.border - sqrt3*LAYOUT.orientation.size < position[0] < settings.screen.width - settings.screen.border + sqrt3*LAYOUT.orientation.size):
            if hexagon.coordinate == mouse_hex_pos:
                #cells.add(hexagon)
                hexagon.draw(position, LAYOUT, settings.screen.py_screen, selected=True)
            else:
                hexagon.draw(position, LAYOUT, settings.screen.py_screen)
            # отображение координат шестиугольников
            if show_coord:
                coord_text = settings.font.render("{}, {}".format(*coordinate), False, WHITE)
                coord_text_rect = coord_text.get_rect()
                coord_text_rect.center = position
                settings.screen.py_screen.blit(coord_text, coord_text_rect)

    # ось q
    pygame.draw.line(settings.screen.py_screen,
                     (255, 0, 0),
                     hexmath.hex_to_pixel(LAYOUT, (0, 0), settings=settings),
                     hexmath.hex_to_pixel(LAYOUT, (1, 0), settings=settings))
    # ось r
    pygame.draw.line(settings.screen.py_screen,
                     (0, 255, 0),
                     hexmath.hex_to_pixel(LAYOUT, (0, 0), settings=settings),
                     hexmath.hex_to_pixel(LAYOUT, (0, 1), settings=settings))
    # границы экрана
    pygame.draw.rect(settings.screen.py_screen, 0,
                     (settings.screen.border,
                      settings.screen.border,
                      settings.screen.width-2*settings.screen.border,
                      settings.screen.height-2*settings.screen.border),
                     3)

def update_screen():
    """Отобразит объекты на экране в определенном порядке"""
    settings.screen.py_screen.fill(BACKGROUND)
    #screen.blit(layer_hex, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    #screen.blit(layer_lines, (0, 0), special_flags=pygame.BLEND_RGBA_MAX)
    #cells.draw(screen)
    pygame.display.update()

def main():
    # координаты существующих шестиугольников
    coordinates = Map({(0, 0): Cell((0, 0)),
                       (1, 0): Cell((1, 0)),
                       (0, 1): Cell((0, 1)),
                       (1, 1): Cell((1, 1))})

    coordinates = mapgen.square_grid(60, 60)

    while settings.running:
        settings.clock.tick()

        check_events()  # управление и ивенты

        # ОТРИСОВКА И ОБНОВЛЕНИЕ ЭКРАНА

        settings.screen.py_screen.fill(BACKGROUND)
        draw_grid(coordinates)
        #update_screen()
        pygame.display.update()

        print("FPS:", settings.clock.get_fps())
        #LAYOUT.print()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
