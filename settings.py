class Settings:
    """ A class to store all the settings for the game. """

    def __init__(self):
        """ Initialise game settings. """

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.BACKGROUND_COLOR = (230, 230, 230)
        self.WINDOW_TITLE = "Space Invaders."

        # Spaceship settings
        self.spaceship_speed = 3.0
        self.SPACESHIP_LIVES = 3

        # Missile settings
        self.missile_speed = 6.0
        self.missile_count = 3

        # Alien ship settings
        self.alien_speed = 3.0
        self.alien_drop_speed = 10
        # Alien direction 1 represents RIGHT; -1 represents LEFT
        self.alien_direction = 1

        # Alien points for scoring
        self.alien_points = 10

        # Game speed up scale.
        self.speed_scale = 1.1
        self.points_scale = 2

    def initialise_dynamic_settings(self):
        """ Initialise settings that have changed throughout game-play """
        self.spaceship_speed = 3.0
        self.missile_speed = 6.0
        self.alien_speed = 3.0
        self.alien_points = 10

    def increase_speed(self):
        self.spaceship_speed *= self.speed_scale
        self.missile_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale
        self.alien_points *= self.points_scale

