import pygame.font
from pygame.sprite import Group

from spaceship import Spaceship


class Scoreboard:
    """ A class to create and manage the scoreboard. """

    def __init__(self, game):
        """ Initialise scoreboard attributes. """
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.game_stats

        # Font settings for scoreboard information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.Font('support_files/retro_font.ttf', 14)

        # create the scoreboard images
        self.prepare_scoreboard()
        self.prepare_high_scoreboard()
        self.prepare_level()
        self.prepare_lives()

    def prepare_scoreboard(self):
        """ Turn scoreboard into a rendered image. """
        score_string = str(f"Score: {{:,}}".format(self.stats.score))
        self.score_image = self.font.render(score_string, True, self.text_color, self.settings.BACKGROUND_COLOR)

        # Position scoreboard at top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prepare_high_scoreboard(self):
        """ Turn the highest score into a rendered image. """
        high_score = str(f"High Score: {{:,}}".format(self.stats.high_score))
        self.high_score_image = self.font.render(high_score, True, self.text_color, self.settings.BACKGROUND_COLOR)

        # Position high score in centre of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prepare_level(self):
        """ Turn the level into a rendered image. """
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.BACKGROUND_COLOR)

        # Position the level under the current score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.score_rect.right

    def prepare_lives(self):
        """ Show how many lives player has remaining. """
        self.player_lives = Group()
        for life_number in range(self.stats.ships_remaining):
            # Use spaceship image to represent life.
            life = Spaceship(self.game)
            life.image = pygame.transform.smoothscale(life.image, (30, 45))
            life.rect.x = 20 + life_number * (life.rect.width / 2)
            life.rect.y = 20
            self.player_lives.add(life)

    def check_high_score(self):
        """ Check for new high score. """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prepare_high_scoreboard()

    def show_scoreboard(self):
        """ Draw scoreboards and current level to the screen. """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.player_lives.draw(self.screen)
