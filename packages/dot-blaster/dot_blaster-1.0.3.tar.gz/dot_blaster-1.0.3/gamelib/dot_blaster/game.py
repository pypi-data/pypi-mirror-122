"""Module to handle the main Game Loop

To test this, run "run_ld49_game" in the CLI

"""
import random
import sys

import pygame

from . import __NAME__, asset_loader, colors
from . import constants as const
from . import image_tools
from .custom_events import GAME_OVER, SCORE_INCREASE
from .enemy_factory import EnemyFactory
from .physics import GamePhysicsHandler
from .planet import Planet
from .player import Player
from .enemy import Enemy
from .score_manager import ScoreManager
from .screen_handler import ScreenHandler
from .ui.title_menu import TitleMenu
from .ui.game_over_screen import GameOverScreen

PLAY_BACKGROUND_MUSIC = False


class GameWindow:
    def __init__(self):
        pygame.display.set_caption(__NAME__)
        self.screen_handler = ScreenHandler()
        self.score_manager = ScoreManager()

        if PLAY_BACKGROUND_MUSIC:
            self.play_background_music()

        self.game_is_running = False
        self.restart = True
        self.main_loop()
        self.game = None

    def play_background_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load(asset_loader.filepath("sfx/music.mp3"))
        pygame.mixer.music.play(-1)  # loop the file

    def main_loop(self):
        while self.restart:
            if not self.game_is_running:
                title_screen = TitleMenu(
                    self.screen_handler.screen, self.start_game
                )
                title_screen.update()

    def start_game(self):
        print("Start game")
        self.game = Game(self.screen_handler, self.score_manager)
        self.game_is_running = True
        self.game.run_game()

        self.restart = self.game.restart  # allow game to control execution
        self.game_is_running = False


class Game:
    def __init__(self, screen_handler: ScreenHandler, score_manger=None):
        self.screen_handler = screen_handler
        self.restart = False
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.physics_handler = GamePhysicsHandler(
            self.screen_handler, const.FPS
        )
        if score_manger:
            self.score_manger = score_manger
        else:
            self.score_manger = ScoreManager()
        self.update_full_screen = False
        self.fullscreen = False
        self.init_data()
        self.init_scene()

    def init_scene(self):
        self.planet = Planet(
            size=const.PLANET_SIZE,
            screen_handler=self.screen_handler,
            color=const.PLANET_COLOR,
            physics_handler=self.physics_handler,
        )
        self.enemy_factory = EnemyFactory(
            screen_handler=self.screen_handler,
            physics_handler=self.physics_handler,
        )
        self.player = Player(
            size=int(self.planet.size * 0.75),
            screen_handler=self.screen_handler,
            physics_handler=self.physics_handler,
        )
        self.game_over_screen = GameOverScreen(
            self.screen_handler, self.score_manger
        )

    def init_data(self):
        self.bgk_image = image_tools.change_image_alpha(
            const.BACKGROUND_IMAGE, 50
        )

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()

        elif event.key == pygame.K_q:  # the X button on the window
            sys.exit()

        elif event.key == pygame.K_p:
            pygame.image.save(
                self.screen_handler.screen,
                f"game_screenshot_{self.clock.tick}.png",
            )

        elif event.key == pygame.K_f:  # the maximise button on the window
            if not self.fullscreen:
                # Full screen needs pygame 2.0.0 for scaled.
                pygame.display.set_mode(
                    (const.WIDTH, const.HEIGHT),
                    pygame.FULLSCREEN | pygame.SCALED,
                )
                self.update_full_screen = True
                self.fullscreen = True
            else:
                pygame.display.set_mode((const.WIDTH, const.HEIGHT))
                self.update_full_screen = True
                self.fullscreen = False

        elif event.key == pygame.K_RETURN and self.game_over:
            self.restart = True

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self.on_keydown(event)

            if event == GAME_OVER:
                self.game_over = True
                self.score_manger.save_highscore()

            if event == SCORE_INCREASE:
                self.score_manger.increase_score()

    def draw_background(self):
        self.screen_handler.screen.fill(const.BACKGROUND_COLOR)
        rect = self.bgk_image.get_rect()
        rect.center = self.screen_handler.center
        self.screen_handler.screen.blit(self.bgk_image, rect)

    def run_game(self):

        while not self.restart:
            self.process_events()
            pressed_keys = pygame.key.get_pressed()

            # Process inputs + update physics
            if not self.game_over:
                self.player.process_input(pressed_keys)
                self.enemy_factory.update()
                self.physics_handler.update()

            # drawing
            self.draw_background()
            self.player.update()
            for go in self.physics_handler.physics_game_objects:
                go.update()
            self.planet.update()
            if not self.game_over:
                self.score_manger.draw_score_on_top_right()
            else:
                self.game_over_screen.draw()

            pygame.display.flip()
            self.clock.tick(const.FPS)

            if self.physics_handler.DEBUG_MODE:
                pygame.display.set_caption(
                    f"fps: {self.clock.get_fps():0.2f}, "
                    f"num obj: {len(self.physics_handler.physics_game_objects):02d}"
                )

        if self.restart:
            self.score_manger.reset_score()
            self.physics_handler.destroy()
            Enemy.STATIC_NUM_ENEMIES = 0
            self.init_scene()
            self.restart = False
            self.game_over = False
            self.run_game()
