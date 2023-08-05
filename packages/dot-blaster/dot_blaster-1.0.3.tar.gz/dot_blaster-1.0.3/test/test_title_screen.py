import random

import pygame

from dot_blaster import colors
from dot_blaster.constants import FPS, HEIGHT, WIDTH
from dot_blaster.enemy import Enemy
from dot_blaster.physics import GamePhysicsHandler
from dot_blaster.planet import Planet
from dot_blaster.ui import TitleMenu


def start_game_test():
    print("START")


def test_enemy():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    title_menu = TitleMenu(screen, start_game_test)

    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "planet.png")

        # 'planet' in the center of screen
        screen.fill(pygame.Color("black"))
        title_menu.run_game()

        pygame.display.flip()


if __name__ == "__main__":
    test_enemy()
