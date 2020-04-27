class Settings:
    """ A class to store all the settings for the game. """

    def __init__(self):
        """ Initialise game settings. """

        # Screen Settings
        self.screen_width = 0
        self.screen_height = 0
        self.BACKGROUND_COLOR = (230, 230, 230)
        self.WINDOW_TITLE = "Retro Space Invaders."

        # Spaceship settings
        self.SPACESHIP_SPEED = 5

        # Missile settings
        self.missile_speed = 8
        self.missile_width = 3
        self.missile_height = 15
        self.missile_color = (60, 60, 60)
        self.missile_count = 5

        # Alien ship settings
        self.alien_speed = 3.0
        self.alien_drop_speed = 10
        # Alien direction 1 represents RIGHT; -1 represents LEFT
        self.alien_direction = 1

