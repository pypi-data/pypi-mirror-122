import random

import pygame

from dot_blaster import colors
from dot_blaster.constants import FPS, HEIGHT, WIDTH
from dot_blaster.score_manager import ScoreManager


def test_enemy():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    score_manager = ScoreManager()

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

        screen.fill(pygame.Color("black"))
        score_manager.draw_score_on_top_right()

        pygame.display.flip()
        clock.tick(FPS)

        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    test_enemy()
