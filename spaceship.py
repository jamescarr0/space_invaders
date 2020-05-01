import pygame
from pygame.sprite import Sprite


class Spaceship(Sprite):
    """ A class to manage the spaceship. """

    def __init__(self, si_game):
        super().__init__()
        self.settings = si_game.settings
        self.screen = si_game.screen
        self.screen_rect = si_game.screen.get_rect()

        # Load the spaceship image and get its rectangle.
        self.image = pygame.transform.smoothscale((pygame.image.load('images/spaceship.png')), (80, 120))
        self.rect = self.image.get_rect()

        # Start with a new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Continuous movement flags.
        self.moving_right = False
        self.moving_left = False

        self.x = float(self.rect.x)

    def move(self):
        """ Update the spaceship's position. """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.spaceship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.spaceship_speed

        self.rect.x = self.x

    def respawn(self):
        """ Respawn spaceship to center position. """
        # Center spaceship midbottom to screen midbottom position
        self.rect.midbottom = self.screen_rect.midbottom

        # Reset self.x attribute to allow us to track the ships exact position.
        self.x = float(self.rect.x)

    def blitme(self):
        """ blit spaceship to screen. """
        self.screen.blit(self.image, self.rect)
