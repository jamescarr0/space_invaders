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
        self.text_color = self.settings.TEXT_COLOR
        self.font = pygame.font.Font('support_files/retro_font.ttf', 14)

        # Create the scoreboard images
        self.prepare_scoreboard_images()

    def prepare_scoreboard_images(self):
        """ Prepare the scoreboard images. """
        self.prepare_game_score()
        self.prepare_high_score()
        self.prepare_level()
        self.prepare_lives()
        self.prepare_frames_per_second(0.0)

    def _render_image(self, string):
        """ Render passed string as an image, convert to alpha, remove the background color for a transparent
        background and return the rendered image. """
        image = self.font.render(string, True, self.text_color, self.settings.BACKGROUND_COLOR)
        image.convert_alpha()
        image.set_colorkey(self.settings.BACKGROUND_COLOR)
        return image

    def prepare_frames_per_second(self, fps):
        """ Turn FPS into a rendered image. """

        self.fps_str = str(f"fps: {round(fps)}")
        self.fps_image = self._render_image(self.fps_str)
        self.fps_image_rect = self.fps_image.get_rect()
        self.fps_image_rect.top = self.level_rect.bottom + 10
        self.fps_image_rect.right = self.score_rect.right

    def prepare_game_score(self):
        """ Turn scoreboard into a rendered image. """
        score_string = str(f"Score: {{:,}}".format(self.stats.score))
        self.score_image = self._render_image(score_string)

        # Position scoreboard at top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prepare_high_score(self):
        """ Turn the highest score into a rendered image. """
        high_score = str(f"High Score: {{:,}}".format(self.stats.high_score))
        self.high_score_image = self._render_image(high_score)

        # Position high score in centre of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prepare_level(self):
        """ Turn the level into a rendered image. """
        level_str = f"Level: {self.stats.level}"
        self.level_image = self._render_image(level_str)

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
            self.prepare_high_score()

    def show_scoreboard(self):
        """ Draw scoreboards and current level to the screen. """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.fps_image, self.fps_image_rect)
        self.player_lives.draw(self.screen)
