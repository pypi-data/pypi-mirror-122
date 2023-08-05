from typing import Optional

import numpy as np
import pygame
import pymunk
from dot_blaster import colors
from dot_blaster.constants import LASER_LENGTH, LASER_SPEED, LASER_WIDTH

from .screen_handler import ScreenHandler
from .game_object import GameObject
from .physics import CollisionType, GamePhysicsHandler


class Laser(GameObject):
    def __init__(
        self,
        screen_handler: ScreenHandler,
        angle: float,
        color,
        physics_handler: Optional[GamePhysicsHandler] = None,
    ):
        """
        Initialize the laser based on the current position of the player
        """
        self.screen_handler = screen_handler
        self.angle = angle

        self.color = color
        self.speed = LASER_SPEED
        self.r = 50  # separation from center of the sceen # TODO
        self.dir_vector = self.get_direction_vector()
        self.x = self.r * np.cos(self.angle) + self.screen_handler.center[0]
        self.y = self.r * np.sin(self.angle) + self.screen_handler.center[1]
        self.length = LASER_LENGTH
        self.width = LASER_WIDTH

        super().__init__(
            screen_handler=self.screen_handler,
            color=color,
            x=self.x,
            y=self.y,
            physics_handler=physics_handler,
        )

    def get_direction_vector(self):
        return (np.cos(self.angle), np.sin(self.angle))

    def _init_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.x - self.width / 2,
            self.y - self.length / 2,
            self.width,
            self.length,
        )

    def _init_rigid_body(self) -> pymunk.Body:
        rigid_body = pymunk.Body(pymunk.Body.KINEMATIC)
        rigid_body.collision_type = CollisionType.LASER.value
        rigid_body.angle = self.angle + np.pi / 2
        rigid_body.velocity = [
            self.speed * np.cos(self.angle),
            self.speed * np.sin(self.angle),
        ]
        rigid_body.position = pymunk.Vec2d(self.x, self.y)
        return rigid_body

    def _init_collider(self) -> pymunk.Circle:
        col = pymunk.Segment(
            self.rigid_body,
            [0, -self.length / 2],
            [0, self.length / 2],
            self.width,
        )
        col.mass = 1
        col.friction = 0.0
        col.damping = 0.0
        col.elasticity = 0
        col.filter = pymunk.ShapeFilter(
            mask=pymunk.ShapeFilter.ALL_MASKS() ^ CollisionType.ENEMY.value
        )
        return col

    def get_collider_world_bounds(self):
        p1 = self.rigid_body.local_to_world((0, self.length / 2))
        p2 = self.rigid_body.local_to_world((0, -self.length / 2))
        return p1, p2

    def draw(self):
        p1, p2 = self.get_collider_world_bounds()
        self.rect = pygame.draw.line(
            self.screen_handler.screen, self.color, p1, p2, self.width
        )

    def update(self) -> None:
        self.draw()
        if self.is_physics_object:
            (x, y) = self.rigid_body.position
            self.rect.center = x, y
            self.rect.midtop = (
                x + self.dir_vector[0] * self.length / 2,
                y + self.dir_vector[1] * self.length / 2,
            )
            self.handle_collision_with_enemy()

        super().update()
        # If laser leaves the screen, delete it
        if self.distance_to_center > self.screen_handler.half_diag:
            self.destroy()
