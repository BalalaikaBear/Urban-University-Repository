from mapgenerators import *
from checkevents import *

def main():
    # координаты существующих шестиугольников
    coordinates = {(0, 0): Cell((0, 0)),
                   (1, 0): Cell((1, 0)),
                   (0, 1): Cell((0, 1)),
                   (1, 1): Cell((1, 1))}

    coordinates = generate_square_grid(60, 60)

    while running:
        clock.tick()

        check_events()  # управление и ивенты

        # ОТРИСОВКА И ОБНОВЛЕНИЕ ЭКРАНА

        screen.fill((0, 0, 0))
        #draw_grid(coordinates)
        #update_screen()
        pygame.display.update()

        print("FPS:", clock.get_fps())
        #LAYOUT.print()

    pygame.quit()


if __name__ == "__main__":
    main()