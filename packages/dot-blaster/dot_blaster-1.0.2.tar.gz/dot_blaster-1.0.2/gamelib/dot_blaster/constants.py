import pygame

from dot_blaster import colors

import pygame_menu

from . import asset_loader

# SCREEN ARGS
FPS = 50
SCALE = 2
REAL_WIDTH = 360
REAL_HEIGHT = REAL_WIDTH
WIDTH = REAL_WIDTH * SCALE
HEIGHT = REAL_HEIGHT * SCALE

SOUND_VOLUME = 0.4


# Constants for objects

ROTATION_SPEED = 0.1
REFIRE_DELAY = 250  # ms
LASER_SPEED = 800
LASER_LENGTH = 40
LASER_WIDTH = 3
ENEMY_SIZE = 10
MAX_ENEMY_VEL = 90
PLANET_SIZE = 25  # 40
MAX_NUM_ENEMIES_IN_GAME = 10

# COLORS
COL_TYPE1 = colors.MAXIMUM_YELLOW_RED
COL_TYPE2 = colors.ELECTRIC_BLUE
BACKGROUND_COLOR = colors.CYBER_GRAPE
PLANET_COLOR = colors.SPACE_CADET

# FONT ARGS
FONT_MAIN = pygame_menu.font.FONT_MUNRO
FONT_COLOR = colors.WHITE
PTXT_KWARGS = dict(fontname=FONT_MAIN, color=FONT_COLOR)


BACKGROUND_IMAGE_PATH = asset_loader.filepath("sprites/faded_circle.png")
BACKGROUND_IMAGE = asset_loader.load_image("sprites/faded_circle.png")
ICON = asset_loader.load_image("sprites/icon.png")

HIGHSCORE_FILE = "data/highscore.txt"
