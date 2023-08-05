from typing import Callable

from .base_menu import BaseMenu
from ..score_manager import ScoreManager

import pygame_menu


class TitleMenu(BaseMenu):
    def __init__(
        self, screen, start_func: Callable, score_manager=ScoreManager()
    ):
        super(TitleMenu, self).__init__(screen)
        self.main_menu.add.button("Play", start_func)
        self.add_instructions()
        self.main_menu.add.button("Quit", pygame_menu.events.EXIT)
        self.add_score(score_manager)
