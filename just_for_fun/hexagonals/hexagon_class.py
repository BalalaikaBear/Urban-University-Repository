import pygame, math


def hex_corners(position, size):
    corners = []
    x, y = position

    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.pi / 180 * angle_deg
        corners.append((x + size * math.cos(angle_rad), y + size * math.sin(angle_rad)))

    return corners


class Hexagon:
    def __init__(self, color=(0, 0, 255)):
        self.color = color
        self.selected = False  # для изменения цвета при выделении

    def draw(self, screen, position, size):
        if self.selected:
            pygame.draw.circle(screen, (0, 0, 0), position, size)
        else:
            pygame.draw.circle(screen, self.color, position, size)
        pygame.draw.lines(screen, (0, 0, 0), True, hex_corners(position, size))

