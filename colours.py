from collections import namedtuple

Colour = namedtuple("Colour", ["r", "g", "b"])

BACKGROUND = Colour(r=1, g=22, b=39)
SNAKE = Colour(r=69, g=186, b=100)
FOOD = Colour(r=222, g=72, b=64)
TEXT = Colour(r=255, g=255, b=255)