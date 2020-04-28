import pygame.font

class Scoreboard:
    """ A class to create and manage the scoreboard. """

    def __init__(self, game):
        """ Initialise scoreboard attributes. """
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.game_stats

        # Font settings for scoreboard information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # create the scoreboard image
        self.prepare_scoreboard()

    def prepare_scoreboard(self):
        """ Turn scoreboard into a rendered image. """
        score_string = str(f"Score: {{:,}}".format(self.stats.score))
        self.score_image = self.font.render(score_string, True, self.text_color, self.settings.BACKGROUND_COLOR)

        # Position scoreboard at top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_scoreboard(self):
        """ Draw scoreboard to the screen. """
        self.screen.blit(self.score_image, self.score_rect)