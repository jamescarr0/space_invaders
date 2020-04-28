import pygame
from pygame.sprite import Sprite


class SpaceshipMissile(Sprite):
    """ A class to manage the missiles fired from the spaceship. """

    def __init__(self, game):
        """ Create a missile object at the spaceships current position. """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.transform.smoothscale((pygame.image.load('images/missile.png')), (15, 45))
        self.rect = self.image.get_rect()
        self.rect.midtop = game.spaceship.rect.midtop

        # Store the missiles position as a float
        self.y = float(self.rect.y)

    def update(self):
        """ Move the missile up the screen. """
        # set missile speed and update the missiles rect position
        self.y -= self.settings.missile_speed
        self.rect.y = self.y

    def draw_missile(self):
        """ Draw the missile to the screen. """
        self.screen.blit(self.image, self.rect)
