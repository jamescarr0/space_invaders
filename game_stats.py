import os


class GameStats:
    """ A class to track game statistics for Space Invaders. """

    def __init__(self, game):
        """ Init stats """
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self._get_high_score()

    def reset_stats(self):
        """ Reset game statistics """
        self.ships_remaining = self.settings.SPACESHIP_LIVES
        self.score = 0
        self.level = 1

    def _get_high_score(self):
        """ Read high score from file and return an int. If file is empty return a default value of zero. """
        filepath = self.settings.high_score_file

        if os.stat(filepath).st_size == 0:
            return 0
        else:
            with open(filepath) as high_score_file:
                contents = high_score_file.readline()
            return int(contents)
