from abc import abstractmethod

import pygame_menu

from .. import __NAME__  # game name
from .. import constants as const
from .. import image_tools


class BaseMenu:
    def __init__(self, screen, name=__NAME__):
        self.theme = self.make_menu_theme()
        self.main_menu = pygame_menu.Menu(
            width=const.WIDTH,
            height=const.HEIGHT * 0.75,
            title=name,
            theme=self.theme,
        )
        self.instructions_menu = pygame_menu.Menu(
            width=const.WIDTH,
            height=const.HEIGHT * 0.75,
            theme=self.theme,
            title="Instructions",
        )

        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ctr = self.screen_rect[0] / 2, self.screen_rect[1] / 2

        self.bgk_image = image_tools.change_image_alpha(
            const.BACKGROUND_IMAGE, 50
        )

    def make_menu_theme(self):
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.title_font_size = 70
        theme.widget_font_size = 50
        theme.title_bar_style = (
            pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
        )
        theme.widget_padding = 25
        theme.widget_alignment = pygame_menu.pygame_menu.locals.ALIGN_LEFT
        theme.widget_font = const.FONT_MAIN
        theme.title_font = const.FONT_MAIN
        theme.background_color = const.BACKGROUND_COLOR
        theme.title_background_color = const.PLANET_COLOR
        theme.set_background_color_opacity(0.0)
        return theme.copy()

    def add_instructions(self):
        self.main_menu.add.button("Instructions", self.instructions_menu)
        HELP = (
            "Press ENTER switch blaster\n"
            "Press SPACE to shoot\n"
            "Press LEFT/RIGHT to move Player"
        )

        self.instructions_menu.add.label(HELP, max_char=-1, font_size=35)

    def add_score(self, score_manager):
        txt = f"High Score: {score_manager.highscore:03d}"
        self.main_menu.add.label(txt, max_char=-1, font_size=35)

    @abstractmethod
    def add_buttons_to_menu(self, *args):
        pass

    def draw_background(self):
        self.screen.fill(const.BACKGROUND_COLOR)
        rect = self.bgk_image.get_rect()
        rect.center = self.ctr
        self.screen.blit(self.bgk_image, rect)

    def update(self):
        self.main_menu.mainloop(self.screen, self.draw_background)
