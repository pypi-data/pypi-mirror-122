import math

import numpy as np
import pygame
import pymunk

from dot_blaster.constants import COL_TYPE1

from .game_object import GameObject
from .physics import CollisionType, G, planet_gravity

from .sparks import Sparks


class Enemy(GameObject):

    STATIC_NUM_ENEMIES = 0

    def __init__(self, screen_handler, color, size, x, y, physics_handler):
        Enemy.STATIC_NUM_ENEMIES += 1
        self.sparks = None
        super().__init__(
            screen_handler,
            color,
            size,
            x=x,
            y=y,
            physics_handler=physics_handler,
        )

    def _init_rigid_body(self) -> pymunk.Body:
        rigid_body = pymunk.Body(pymunk.Body.KINEMATIC)

        rigid_body.collision_type = CollisionType.ENEMY.value
        rigid_body.position = pymunk.Vec2d(self.x, self.y)
        rigid_body.velocity_func = planet_gravity

        # Set the enemy's velocity to put it into a circular orbit from its
        # starting position. (dampening prevents circular orbit)
        r = rigid_body.position.get_distance(self.screen_handler.center)
        v = math.sqrt(G / r) / r

        # Reverse direction for enemies with COLOR1
        if self.color == COL_TYPE1:
            v *= -1
        vec_to_center = rigid_body.position - pymunk.Vec2d(
            *self.screen_handler.center
        )

        circular_velocity = v * vec_to_center.perpendicular()

        factor_off_orbit = np.random.uniform(0.7, 0.95)
        rigid_body.velocity = circular_velocity * factor_off_orbit

        rigid_body.angular_velocity = v
        rigid_body.angle = math.atan2(
            rigid_body.position.y, rigid_body.position.x
        )
        return rigid_body

    def _init_collider(self) -> pymunk.Circle:
        col = pymunk.Circle(self.rigid_body, self.radius)
        col.mass = 10
        col.friction = 0.7
        col.damping = 0.98
        col.elasticity = 1
        col.filter = pymunk.ShapeFilter(categories=CollisionType.ENEMY.value)
        if self.physics_handler.DEBUG_MODE:
            col.color = pygame.Color("white")  # colors the collider
        return col

    def update(self):
        if self.alive:
            super().update()
            # If enemy leaves (twice the distance to) the screen, delete it
            if self.distance_to_center > 2 * self.screen_handler.half_diag:
                self.destroy()
        else:
            self.sparks.update()
            if not self.sparks.alive:
                self.destroy()

    def destroy(self) -> None:
        Enemy.STATIC_NUM_ENEMIES -= 1
        super().destroy()

    def death_anim_and_destroy(self):
        if self.alive:
            self.sparks = self.create_sparks()
            self.alive = False

    def create_sparks(self):
        x, y = self.rigid_body.position
        return Sparks(
            self.screen_handler.screen,
            color=self.color,
            loc=[x, y],
            angle_range=(0, 360),
            speed_range=(1, 4),
            scale=1,
            num_sparks=10,
        )
