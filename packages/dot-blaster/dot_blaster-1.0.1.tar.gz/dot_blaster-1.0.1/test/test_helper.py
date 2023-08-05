import pygame

from dot_blaster import colors


def make_test_screen(test_name):
    pygame.init()

    width = 800
    heigth = 600
    screen = pygame.display.set_mode((width, heigth))
    screen.fill(colors.BLACK)
    pygame.display.set_caption(test_name)
    return screen


def should_i_quit():
    # Check if user closed window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return True
    return False


def main_runner(screen, func_list, func_args):
    running = True
    while running:
        if should_i_quit():
            running = False

        for f, args in zip(func_list, func_args):
            f(args)

        pygame.display.flip()
