"""Game main module

Contains entry point used by the run_game.py script
"""

import pygame

from . import game


def main():
    """main entry point"""
    pygame.init()
    game.GameWindow()
