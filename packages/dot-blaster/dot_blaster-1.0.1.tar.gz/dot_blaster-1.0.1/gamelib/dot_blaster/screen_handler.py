from typing import Tuple

import numpy as np
import pygame

from . import __NAME__
from . import constants as const


class ScreenHandler:
    def __init__(self):
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption(__NAME__)
        pygame.display.set_icon(const.ICON)
        self.rect = self.screen.get_rect()

    @property
    def size(self) -> Tuple[int, int]:
        return self.screen.get_size()

    @property
    def center(self) -> Tuple[int, int]:
        return self.size[0] / 2, self.size[1] / 2

    @property
    def half_diag(self) -> float:
        return np.sqrt(sum([x * x / 4 for x in self.size]))

    @property
    def diag(self) -> float:
        return np.sqrt(2) * self.size[0]

    def top(self, fraction_from_top=0) -> Tuple[int, int]:
        """fraction needs to be in [0,1]"""
        w, h = self.size
        return w / 2, int(h * fraction_from_top)

    def bot(self, fraction_from_bot=0) -> Tuple[int, int]:
        """fraction needs to be in [0,1]"""
        w, h = self.size
        return w / 2, int(h - h * fraction_from_bot)
