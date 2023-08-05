import random

import pygame

from dot_blaster import colors
from dot_blaster.constants import FPS, HEIGHT, WIDTH
from dot_blaster.game import Game
from dot_blaster.physics import GamePhysicsHandler
from dot_blaster.planet import Planet
from dot_blaster.screen_handler import ScreenHandler


def test_game_scene():
    pygame.init()
    screen = ScreenHandler()
    game = Game(screen)
    game_is_running = True
    game.run_game()


if __name__ == "__main__":
    test_game_scene()
