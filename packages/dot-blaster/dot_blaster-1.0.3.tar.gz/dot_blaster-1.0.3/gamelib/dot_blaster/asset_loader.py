"""Simple asset loader module.

Loads data files from the "assets" directory shipped with a game.

"""

import os

import pygame

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, "assets"))


def filepath(filename):
    """Determine the path to a file in the assets directory."""
    return os.path.join(data_dir, filename)


def load(filename, mode="rb"):
    """Open a file in the data directory.

    "mode" is passed as the second arg to open().
    """
    return open(os.path.join(data_dir, filename), mode)


def load_image(name):
    img = pygame.image.load(filepath(name))
    return img
