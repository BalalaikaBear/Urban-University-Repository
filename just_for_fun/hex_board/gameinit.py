import pygame
from settings import *

# инициализация
pygame.init()
pygame.font.init()

# настройки стандартных элементов pygame
screen = pygame.display.set_mode((settings.screen.width, settings.screen.height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 14)

# слои экрана
layer_hex = pygame.Surface((settings.screen.width, settings.screen.height))
layer_lines = pygame.Surface((settings.screen.width, settings.screen.height))
layer_text = pygame.Surface((settings.screen.width, settings.screen.height))