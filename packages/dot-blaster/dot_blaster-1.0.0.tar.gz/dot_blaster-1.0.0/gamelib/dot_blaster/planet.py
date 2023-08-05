import pygame
import pymunk

from .game_object import GameObject
from .physics import CollisionType


class Planet(GameObject):
    def _init_rigid_body(self) -> pymunk.Body:
        rigid_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rigid_body.collision_type = CollisionType.PLANET.value
        rigid_body.position = pymunk.Vec2d(self.x, self.y)
        return rigid_body

    def _init_collider(self) -> pymunk.Circle:
        col = pymunk.Circle(self.rigid_body, self.size)
        col.mass = 10
        col.friction = 0.7
        col.damping = 0.9
        col.elasticity = 1
        if self.physics_handler.DEBUG_MODE:
            col.color = pygame.Color("red")  # colors the collider
        return col
