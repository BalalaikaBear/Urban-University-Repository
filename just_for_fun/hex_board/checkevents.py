from gameinit import *
from coordinates import *

running = True

# проверка нажатия кнопок
left_pressed = False
right_pressed = False
up_pressed = False
down_pressed = False
turn_counterclockwise = False
turn_clockwise = False

def check_events():
    """Управление"""
    global running
    global left_pressed
    global right_pressed
    global up_pressed
    global down_pressed
    global turn_counterclockwise
    global turn_clockwise

    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            running = False

        # нажатие клавиши
        if event.type == pygame.KEYDOWN:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = True
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = True
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = True
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = True
            if event.key == pygame.K_q:
                turn_counterclockwise = True
            if event.key == pygame.K_e:
                turn_clockwise = True

            # возвращение на начальную клетку
            if event.key == pygame.K_h:
                LAYOUT.set_layout(layout_flat)

        # отжатие клавиши
        if event.type == pygame.KEYUP:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                left_pressed = False
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                right_pressed = False
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                up_pressed = False
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                down_pressed = False
            if event.key == pygame.K_q:
                turn_counterclockwise = False
            if event.key == pygame.K_e:
                turn_clockwise = False

        # вращение колесика мыши
        if event.type == pygame.MOUSEWHEEL:
            # приближение/отдаление камеры
            LAYOUT.scale(1 + event.y * settings.camera.scale)


    # УПРАВЛЕНИЕ КАМЕРОЙ
    # перемещение
    if left_pressed and not right_pressed:
        LAYOUT.translate((1, 0))
    if right_pressed and not left_pressed:
        LAYOUT.translate((-1, 0))
    if up_pressed and not down_pressed:
        LAYOUT.translate((0, 1))
    if down_pressed and not up_pressed:
        LAYOUT.translate((0, -1))
    # вращение
    if turn_clockwise and not turn_counterclockwise:
        LAYOUT.rotate(-1)
    if turn_counterclockwise and not turn_clockwise:
        LAYOUT.rotate(1)
