from . import constants as const
from .asset_loader import load
from .colors import WHITE
from .constants import HIGHSCORE_FILE
from .ui import ptext


class ScoreManager:
    def __init__(self):
        self._points = 0
        self.archived_score = self.read_archived_score()
        self.highscore = self.archived_score

    def increase_score(self):
        self._points += 1
        if self._points > self.highscore:
            self.highscore = self._points

    def read_archived_score(self):
        try:
            with load(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def draw_score_on_top_right(self):
        text = f"Score {self._points:03d}"
        ptext.draw(text, topleft=(3, 3), **const.PTXT_KWARGS)

    def save_highscore(self):
        with load(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.highscore))

    def reset_score(self):
        self._points = 0
