import random

import pygame

from dot_blaster import colors
from dot_blaster.constants import FPS, HEIGHT, WIDTH
from dot_blaster.enemy import Enemy
from dot_blaster.physics import GamePhysicsHandler
from dot_blaster.planet import Planet


def test_enemy():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    physics_handler = GamePhysicsHandler(screen, FPS)
    planet = Planet(
        size=40,
        screen=screen,
        color=colors.YELLOW,
        physics_handler=physics_handler,
    )

    for i in range(30):
        Enemy(
            x=random.randint(0, WIDTH),
            y=random.randint(0, HEIGHT),
            size=10,
            screen=screen,
            physics_handler=physics_handler,
            color=colors.RED,
        )

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
        for go in physics_handler.physics_game_objects:
            go.run_game()
        physics_handler.run_game()

        pygame.display.flip()
        clock.tick(FPS)

        pygame.display.set_caption("fps: " + str(clock.get_fps()))


if __name__ == "__main__":
    test_enemy()
