import pygame

from dot_blaster.score_manager import ScoreManager
from dot_blaster.screen_handler import ScreenHandler
from dot_blaster.ui.game_over_screen import GameOverScreen

from dot_blaster import constants as const


def test_2():
    pygame.init()
    screen_mgr = ScreenHandler()
    score = ScoreManager()
    go = GameOverScreen(screen_mgr, score)
    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
            ):
                exit()
        screen_mgr.screen.fill(pygame.Color("purple"))
        go.draw()
        pygame.display.flip()


if __name__ == "__main__":
    test_2()
