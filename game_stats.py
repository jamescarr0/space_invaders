class GameStats:
    """ Track game statistics for Space Invaders. """

    def __init__(self, game):
        """ Init stats """
        self.settings = game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """ Reset game statistics """
        self.ships_remaining = self.settings.SPACESHIP_LIVES