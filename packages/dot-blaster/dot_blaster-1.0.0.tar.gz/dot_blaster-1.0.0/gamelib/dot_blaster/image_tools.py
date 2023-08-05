import pygame


def colorize_image(image, new_color):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(new_color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image


def change_image_alpha(image, alpha=128):
    image = image.copy()
    image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    return image
