import pygame


class Spaceship:
    """ A class to manage the spaceship """

    def __init__(self, si_game):
        self.settings = si_game.settings
        self.screen = si_game.screen
        self.screen_rect = si_game.screen.get_rect()

        # Load the spaceship image and get its rectangle.
        self.image = pygame.transform.smoothscale((pygame.image.load('images/boris.png')), (120, 180))
        self.image_rect = self.image.get_rect()

        # Start with a new ship at the bottom center of the screen.
        self.image_rect.midbottom = self.screen_rect.midbottom

        # Continuous movement flags.
        self.moving_right = False
        self.moving_left = False

        self.x = float(self.image_rect.x)

    def move(self):
        """ Update the spaceship's position based on the continuous movement flags """
        if self.moving_right and self.image_rect.right < self.screen_rect.right:
            self.x += self.settings.SPACESHIP_SPEED
        if self.moving_left and self.image_rect.left > 0:
            self.x -= self.settings.SPACESHIP_SPEED

        self.image_rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.image_rect)
