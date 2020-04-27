import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Class to manage a single alien ship in the fleet. """

    def __init__(self, game):
        """ Initialise the alien ship and assign a starting position """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the alien ship image and set its rect attribute.
        self.image = pygame.image.load('images/germ.png')
        self.rect = self.image.get_rect()

        # Start each new alien ship near the top left corner of the screen.
        # Space around ship is equal to its size
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien ships exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """ Move the alien right or left across the screen """
        self.x += (self.settings.alien_speed * self.settings.alien_direction)
        self.rect.x = self.x

    def check_screen_edge(self):
        """ Return True if alien ship is at the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

