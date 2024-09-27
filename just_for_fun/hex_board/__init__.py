import math
from hexmath import *
from coordinates import Orientation, Layout
from settings import Player

sqrt3 = math.sqrt(3)

player = Player('Admin')

# стартовая ориентация ячеек
layout_flat = Orientation(numpy.array([[3/2, 0, 0],
                                      [sqrt3/2, sqrt3, 0],
                                      [0, 0, 1]]),
                          angle=0,
                          size=30)

# применяемая система координат (перемещение, масштабирование, начальное положение)
LAYOUT = Layout(layout_flat, player)