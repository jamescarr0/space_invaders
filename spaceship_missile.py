import pygame
from pygame.sprite import Sprite
from random import randint

class SpaceshipMissile(Sprite):
    """ A class to manage the missiles fired from the spaceship. """

    def __init__(self, game):
        """ Create a missile object at the spaceships current position. """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Create a missile and set the correct position
        random_number = randint(1, 4)
        if random_number == 1:
            self.image = pygame.transform.smoothscale((pygame.image.load('images/loo_roll.png')), (70, 60))
        elif random_number == 2:
            self.image = pygame.image.load('images/needle.png')
        elif random_number == 3:
            self.image = pygame.image.load('images/pound.png')
        else:
            self.image = pygame.transform.smoothscale((pygame.image.load('images/soap.png')), (60, 50))
        self.rect = self.image.get_rect()
        self.rect.midtop = game.spaceship.image_rect.midtop

        # Store the missiles position as a float
        self.y = float(self.rect.y)

    def update(self):
        """ Move the missile up the screen. """
        # set missile speed and update the missiles rect position
        self.y -= self.settings.missile_speed
        self.rect.y = self.y

    def draw_missile(self):
        """ Draw the missile to the screen. """
        #pygame.draw.rect(self.screen, self.settings.missile_color, self.missile_rect)
        self.screen.blit(self.image, self.rect)
