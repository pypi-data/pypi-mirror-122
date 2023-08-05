import math
import random

import pygame


class Spark:
    def __init__(self, loc, angle, speed, color, scale=1):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True

    def point_towards(self, angle, rate):
        rotate_direction = (
            (angle - self.angle + math.pi * 3) % (math.pi * 2)
        ) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sing = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [
            math.cos(self.angle) * self.speed * dt,
            math.sin(self.angle) * self.speed * dt,
        ]

    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        # a bunch of options to mess around with relating to angles...
        # self.point_towards(math.pi / 2, 0.02)
        # self.velocity_adjust(0.975, 0.2, 8, dt)
        # self.angle += 0.1

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        if self.alive:
            points = [
                [
                    self.loc[0]
                    + math.cos(self.angle) * self.speed * self.scale,
                    self.loc[1]
                    + math.sin(self.angle) * self.speed * self.scale,
                ],
                [
                    self.loc[0]
                    + math.cos(self.angle + math.pi / 2)
                    * self.speed
                    * self.scale
                    * 0.3,
                    self.loc[1]
                    + math.sin(self.angle + math.pi / 2)
                    * self.speed
                    * self.scale
                    * 0.3,
                ],
                [
                    self.loc[0]
                    - math.cos(self.angle) * self.speed * self.scale * 3.5,
                    self.loc[1]
                    - math.sin(self.angle) * self.speed * self.scale * 3.5,
                ],
                [
                    self.loc[0]
                    + math.cos(self.angle - math.pi / 2)
                    * self.speed
                    * self.scale
                    * 0.3,
                    self.loc[1]
                    - math.sin(self.angle + math.pi / 2)
                    * self.speed
                    * self.scale
                    * 0.3,
                ],
            ]
            pygame.draw.polygon(surf, self.color, points)


class Sparks:
    def __init__(
        self,
        screen,
        color,
        loc=[0, 0],
        angle_range=(0, 360),
        speed_range=(2, 4),
        scale=1,
        num_sparks=20,
        loop=False,
    ):
        self.num_sparks = num_sparks
        self.screen = screen
        self.loc = loc
        self.angle_range = angle_range
        self.speed_range = speed_range
        self.scale = scale
        self.color = color
        self.sparks_list = []
        self.alive = False
        self.loop = False

        self.generate_sparks()

    def generate_sparks(self):
        for _ in range(self.num_sparks):
            self.sparks_list.append(self.generate_one_spark())
        self.alive = True

    def generate_one_spark(self):
        return Spark(
            loc=self.loc.copy(),
            angle=math.radians(
                random.randint(self.angle_range[0], self.angle_range[1])
            ),
            speed=random.randint(self.speed_range[0], self.speed_range[1]),
            color=self.color,
            scale=self.scale,
        )

    def update(self):
        if self.alive:
            for i, spark in sorted(enumerate(self.sparks_list), reverse=True):
                spark.move(1)
                spark.draw(self.screen)
                if not spark.alive:
                    self.sparks_list.pop(i)

            if len(self.sparks_list) == 0:
                self.alive = False
