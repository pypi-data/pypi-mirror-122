"""Draw on top of Game"""
import pygame

from . import ptext
from .. import constants as const

TITLE = "GAME OVER"
INSTRUCTION_TEXT = "ENTER to restart / ESQ to quit"
CURRENT_SCORE = "Your Score: {:03d}"
HIGH_SCORE = "High Score: {:03d}"

TITLE_FONT_SIZE = 80
SCORE_FONT_SIZE = 50
INSTRUCTION_SIZE = 40


class GameOverScreen:
    def __init__(self, screen_handler, score_manager, opacity=0.5):
        self.scrn_hdlr = screen_handler
        self.score_manager = score_manager
        self.extra_kwargs = dict(
            align="middle",
            owidth=0.5,
            ocolor=const.colors.BLACK,
        )
        self.title_kwargs = dict(
            shadow=(0.5, 0.5),
            scolor=const.colors.BLACK,
        )
        self.opacity = opacity

    def draw_rect_alpha(self):
        color = (0, 0, 0, 255 * self.opacity)
        rect = self.scrn_hdlr.rect
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        self.scrn_hdlr.screen.blit(shape_surf, rect)

    def draw(self):
        """
        Rect with alpha to blur game
        Game over text
        High score text
        Restart text
        """

        self.draw_rect_alpha()

        ptext.draw(
            TITLE,
            fontsize=TITLE_FONT_SIZE,
            center=self.scrn_hdlr.top(0.2),
            **const.PTXT_KWARGS,
            **self.extra_kwargs,
            **self.title_kwargs,
        )

        ptext.draw(
            CURRENT_SCORE.format(self.score_manager._points),
            fontsize=SCORE_FONT_SIZE,
            center=self.scrn_hdlr.top(0.4),
            **const.PTXT_KWARGS,
            **self.extra_kwargs,
        )

        ptext.draw(
            HIGH_SCORE.format(self.score_manager.highscore),
            fontsize=SCORE_FONT_SIZE,
            center=self.scrn_hdlr.top(0.5),
            **const.PTXT_KWARGS,
            **self.extra_kwargs,
        )

        ptext.draw(
            INSTRUCTION_TEXT,
            fontsize=INSTRUCTION_SIZE,
            center=self.scrn_hdlr.bot(0.3),
            **const.PTXT_KWARGS,
            **self.extra_kwargs,
        )
