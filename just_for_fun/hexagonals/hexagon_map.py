import pygame, math
from hexagon_class import Hexagon

pygame.init()
pygame.font.init()

BACKGROUND = (200, 200, 200)
WHITE = (255,255,255)

WIDTH = 1000
HEIGHT = 1000
HEXAGON_SIZE = 50
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)

running = True

CAMERA_SPEED = 10
camera_dx = 0
camera_dy = 0
CAMERA_POS = [0, 0]

def check_events():
    """
    Управление
    """
    global running, camera_dx, camera_dy

    for event in pygame.event.get():
        # закрытие игры
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                camera_dx = -CAMERA_SPEED
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                camera_dx = CAMERA_SPEED
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                camera_dy = -CAMERA_SPEED
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                camera_dy = CAMERA_SPEED

        if event.type == pygame.KEYUP:
            # перемещение камеры
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                camera_dx = 0
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                camera_dx = 0
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                camera_dy = 0
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                camera_dy = 0


def draw_grid(coordinates):
    """
    Отрисовка поля
    """
    show_coord = True  # отображение координат шестиугольников

    for coordinate, hexagon in coordinates.items():
        position = coord_to_pos(*coordinate, *CAMERA_POS)  # положение на экране
        hexagon.draw(screen, position, HEXAGON_SIZE)  # отрисовка шестиугольника

        if show_coord:  # отображение координат шестиугольников
            coord_text = font.render("{}, {}".format(*coordinate), False, WHITE)
            coord_text_rect = coord_text.get_rect()
            coord_text_rect.center = position
            screen.blit(coord_text, coord_text_rect)

    selected_hexagon = pixel_to_coord(*pygame.mouse.get_pos(), *CAMERA_POS)
    print(selected_hexagon)
    if coordinates.get(selected_hexagon):  # если такой шестиугольник есть
        coordinates[selected_hexagon].selected = True  # выделить его


def coord_to_pos(q, r, camera_x, camera_y):
    """
    Преобразование координат шестиугольников в положение на экране
    """
    x = q * 3/2 * HEXAGON_SIZE + WIDTH // 2 + camera_x  # = 3/4 * width + pos
    y = (q * math.sqrt(3)/2 + r * math.sqrt(3)) * HEXAGON_SIZE + HEIGHT // 2 + camera_y  # = height + pos
    return x, y


def pixel_to_coord(x, y, camera_x, camera_y):
    """
    Преобразование пикселя на экране в координату шестиугольника
    """
    q = ((x + camera_x) * 2/3) / HEXAGON_SIZE
    r = ((x + camera_x) * -1/3 + (y + camera_y) * math.sqrt(3)/3) / HEXAGON_SIZE
    return axial_round(q, r)


def axial_round(q, r):
    return cube_to_axial(*cube_round(*axial_to_cube(q, r)))


def axial_to_cube(q, r):
    return q, r, -q-r


def cube_to_axial(q, r, s):
    return q, r


def cube_round(q, r, s):
    round_q, round_r, round_s = round(q), round(r), round(s)
    q_diff, r_diff, s_diff = abs(round_q - q), abs(round_r - r), abs(round_s - s)

    if q_diff > r_diff and q_diff > s_diff:
        round_q = -round_r - round_s
    elif r_diff > s_diff:
        round_r = -round_q - round_s
    else:
        round_s = -round_q - round_r

    return round_q, round_r, round_s


def main():
    # координаты существующих шестиугольников
    coordinates = {(0, 0): Hexagon(),
                   (0, -1): Hexagon((0, 255, 0)),
                   (0, 1): Hexagon(),
                   (1, 0): Hexagon((255, 0, 0))}

    while running:
        clock.tick(FPS)

        check_events()  # управление и ивенты

        # перемещение камеры
        CAMERA_POS[0] += camera_dx
        CAMERA_POS[1] += camera_dy

        # отрисовка и обновление экрана
        screen.fill(BACKGROUND)
        draw_grid(coordinates)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()