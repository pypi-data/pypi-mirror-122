import numpy as np
import pygame

from . import constants as const
from .enemy import Enemy
from .physics import GamePhysicsHandler


class EnemyFactory(object):
    def __init__(self, screen_handler, physics_handler):
        self.screen_handler = screen_handler
        self.physics_handler = physics_handler
        self.r = self.screen_handler.diag / 2.0
        self.num_enemies_per_wave = 2
        self.spawn_radius = [0.8 * self.r, self.r]
        self.start_time = pygame.time.get_ticks()
        self.max_number_enemies_in_game = const.MAX_NUM_ENEMIES_IN_GAME
        self.wave_number = 1
        self.duration = 0

        self.reset()

    def reset(self):
        const.MAX_ENEMY_VEL = 90
        self.num_enemies = 2
        self.spawn_radius = [0.8 * self.r, self.r]
        self.start_time = pygame.time.get_ticks()
        self.max_number_enemies_in_game = const.MAX_NUM_ENEMIES_IN_GAME
        self.wave_number = 1
        self.duration = 0
        for _ in range(3):  # wave 1
            self.create_new_enemy(const.COL_TYPE1)

    def update_duration(self):
        self.duration = pygame.time.get_ticks() - self.start_time

    def update(self):
        self.update_duration()
        # Only have waves show up on odd multiples of 10
        wave_index = int(self.duration / 2500)
        if (wave_index % 2 == 1) & (wave_index > self.wave_number):
            self.wave_number += 1
            self.spawn_wave()

    def spawn_wave(self):
        if self.duration < 15000:  # 15s
            self.num_enemies_per_wave = 2
        elif self.duration < 30000:  # 30s
            self.num_enemies_per_wave = 3
            self.spawn_radius = [self.r * 0.8, self.r * 1.1]
        elif self.duration < 45000:  # 45s
            self.max_number_enemies_in_game = const.MAX_NUM_ENEMIES_IN_GAME * 2
            self.num_enemies_per_wave = 6
            self.spawn_radius = [self.r * 0.8, self.r * 1.6]
        elif self.duration < 60000:  # 1min
            const.MAX_ENEMY_VEL = 100

        count_spawned = 0
        for _ in range(self.num_enemies_per_wave):
            spawned = self.create_new_enemy(self.pick_color())
            if spawned:
                count_spawned += 1
        print(
            f"Wave # {self.wave_number}: Num spawned {count_spawned} ({Enemy.STATIC_NUM_ENEMIES}/{self.max_number_enemies_in_game} enemies)"
        )

    def pick_color(self):
        if self.duration < 8000:  # 8s
            return const.COL_TYPE1
        else:
            return [const.COL_TYPE1, const.COL_TYPE2][np.random.choice(2)]

    def create_new_enemy(self, color):
        if self.max_number_enemies_in_game > Enemy.STATIC_NUM_ENEMIES:

            r_draw = np.random.uniform(
                self.spawn_radius[0], self.spawn_radius[1]
            )
            theta = 2 * np.pi * np.random.rand()

            (ctr_x, ctr_y) = self.screen_handler.center

            Enemy(
                x=r_draw * np.cos(theta) + ctr_x,
                y=r_draw * np.sin(theta) + ctr_y,
                size=const.ENEMY_SIZE,
                screen_handler=self.screen_handler,
                physics_handler=self.physics_handler,
                color=color,
            )
            return True
        return False
