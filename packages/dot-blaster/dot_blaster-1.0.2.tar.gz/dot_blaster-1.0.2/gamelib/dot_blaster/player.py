from typing import Optional

import numpy as np
import pygame

from dot_blaster.constants import (
    COL_TYPE1,
    COL_TYPE2,
    REFIRE_DELAY,
    ROTATION_SPEED,
)
from dot_blaster.laser import Laser

from .game_object import GameObject
from .physics import GamePhysicsHandler
from .screen_handler import ScreenHandler


### Create the triangle character here
class Player(GameObject):
    def __init__(
        self,
        size: int,
        screen_handler: ScreenHandler,
        x: Optional[int] = None,
        y: Optional[int] = None,
        physics_handler: Optional[GamePhysicsHandler] = None,  # Not optional!
    ):
        """
        Initialize the player, which is a rotating triangle.
        Set the initial color, shape, and orientation.
        """
        super().__init__(
            size=size,
            screen_handler=screen_handler,
            color=COL_TYPE1,  # initial color
            x=x,
            y=y,
            physics_handler=physics_handler,
        )
        self.screen_handler = screen_handler
        self.physics_handler = physics_handler
        self.refire_delay = REFIRE_DELAY  # ms
        self.previous_fire_time = 0
        self.theta = 0
        self.color_change_allowed = False
        self.rotation_speed = ROTATION_SPEED
        self.aspect_ratio = 2  # height / width of isosceles triangle
        self.relative_vertices = self.get_relative_vertices()

    def get_relative_vertices(self):
        """
        Calculate the initial vertex coordinates from the aspect ratio and size
        """
        unscaled_coords = [(-1, 0), (1, 0), (0, self.aspect_ratio)]
        relative_vertices = [
            [self.size * coord[0], self.size * coord[1]]
            for coord in unscaled_coords
        ]
        return relative_vertices

    def draw(self):
        """
        Function to draw (or redraw) the triangle
        """
        coordinates = [
            [sum(coords) for coords in zip((self.x, self.y), vertex)]
            for vertex in self.relative_vertices
        ]
        pygame.draw.polygon(
            self.screen_handler.screen, self.color, coordinates, 0
        )

    def process_input(self, pressed_keys):
        """
        Update the player state depending on which keys are pressed"""

        # If left or right arrow pressed, apply rotation
        if pressed_keys[pygame.K_LEFT] | pressed_keys[pygame.K_RIGHT]:
            self.rotate(pressed_keys)

        # If spacebar pressed, fire laser
        if pressed_keys[pygame.K_SPACE]:
            self.fire_laser()

        # If enter pressed, switch mode (only if enter is newly pressed)
        if pressed_keys[pygame.K_RETURN]:
            if self.color_change_allowed:
                self.switch_color()
                self.color_change_allowed = False
        else:  # enter key is unpressed, allow color change again
            self.color_change_allowed = True

    def rotate(self, pressed_keys):
        """
        Rotate the triangle a fixed amount
        """
        dtheta = 0
        # Calculate change in theta
        if pressed_keys[pygame.K_RIGHT]:
            dtheta = self.rotation_speed
        if pressed_keys[pygame.K_LEFT]:
            dtheta = -self.rotation_speed

        # Update current angle
        self.theta += dtheta
        self.relative_vertices = [
            pygame.math.Vector2(p).rotate_rad(dtheta)
            for p in self.relative_vertices
        ]

    def switch_color(self):
        if self.color == COL_TYPE1:
            self.color = COL_TYPE2
        elif self.color == COL_TYPE2:
            self.color = COL_TYPE1
        else:
            raise Exception("Colors not specified correctly for player")

    def fire_laser(self):
        # Calculate if the delay is enough between the previous shot
        current_fire_time = pygame.time.get_ticks()
        if (current_fire_time - self.previous_fire_time) > self.refire_delay:
            # If firing, reset the previous fire time
            self.previous_fire_time = current_fire_time

            radius = self.aspect_ratio * self.size
            laser = Laser(
                screen_handler=self.screen_handler,
                physics_handler=self.physics_handler,
                color=self.color,
                angle=self.theta + np.pi / 2,
            )  # TODO: remove size later
            laser.draw()
