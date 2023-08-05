import math
import random

import pygame
from dot_blaster.sparks import Spark, Sparks
import sys


def update_single_spark_list(sparks, screen):
    for i, spark in sorted(enumerate(sparks), reverse=True):
        spark.move(1)
        spark.draw(screen)
        if not spark.alive:
            sparks.pop(i)


def create_spk(screen):
    return Spark(
        loc=list(screen.get_rect().center),
        angle=math.radians(random.randint(0, 360)),
        speed=random.randint(1, 4),
        color=(255, 255, 255),
        scale=1,
    )


def test_sparks():
    clock = pygame.time.Clock()

    pygame.init()
    pygame.display.set_caption("sparks_test")
    screen = pygame.display.set_mode((500, 500))

    sparks = []
    start_time = pygame.time.get_ticks()

    s = Sparks(
        screen,
        color=(255, 255, 255),
        loc=[200, 200],
        angle_range=(0, 360),
        speed_range=(1, 4),
        scale=1,
        num_sparks=10,
        loop=True,
    )

    sparks = [create_spk(screen) for i in range(10)]

    while True:
        # Background --------------------------------------------- #
        screen.fill((0, 0, 0))

        # update_single_spark_list(sparks ,screen)
        # sparks.append(
        #     Spark(
        #         loc=list(screen.get_rect().center),
        #         angle=math.radians(random.randint(0, 360)),
        #         speed=random.randint(1, 4),
        #         color=(255, 255, 255),
        #         scale=1
        #     )
        # )

        duration = pygame.time.get_ticks() - start_time

        wave_index = int(duration / 2500)

        if s:
            if s.alive:
                s.update()
            else:
                print(f"s dead")
                s = None

        # else:
        #     print("Restarting")
        #     s.generate_sparks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    test_sparks()
