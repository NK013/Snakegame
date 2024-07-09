from collections import namedtuple

Colour = namedtuple("Colour", ["r", "g", "b"])

BACKGROUND = Colour(1, 22, 39)
BACKGROUND_PAUSE = Colour(5, 39, 66)
BACKGROUND_STARTMENU = Colour(20, 46, 9)
BACKGROUND_GAMEOVER = Colour(41, 9, 8)

SNAKE = Colour(69, 186, 100)
FOOD = Colour(222, 72, 64)

TEXT = Colour(255, 255, 255)