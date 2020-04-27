import sys
import pygame

from settings import Settings
from spaceship import Spaceship
from spaceship_missile import SpaceshipMissile
from alien import Alien


class SpaceInvaders:
    """ General class to manage game assets and behaviour. """

    def __init__(self):
        """ Initialise and create objects """
        self.settings = Settings()

        pygame.init()
        pygame.display.set_caption(self.settings.WINDOW_TITLE)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.spaceship = Spaceship(self)

        self.missiles = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_alien_fleet()

    def run_game(self):
        """ Run game - Begin main loop for game. """
        while True:
            self._check_events()
            self.spaceship.move()
            self._update_missiles()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """ Watch for, and respond to keyboard and mouse events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keyup_events(self, event):
        """ Respond to key releases. """
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.spaceship.moving_left = False

    def _check_keydown_events(self, event):
        """ Respond to key presses. """

        # Quit Game
        if event.key == pygame.K_q:
            sys.exit()

        # Fire Missile
        if event.key == pygame.K_SPACE:
            self._fire_missile()

        # Movement
        if event.key == pygame.K_RIGHT:
            self.spaceship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.spaceship.moving_left = True

    def _fire_missile(self):
        """ Create a new missile, and add it to the missiles sprite group. """
        if len(self.missiles) < self.settings.missile_count:
            new_missile = SpaceshipMissile(self)
            self.missiles.add(new_missile)

    def _update_missiles(self):
        """ Update missile positions and remove missiles that are off the screen. """
        self.missiles.update()
        for missile in self.missiles.copy():
            if missile.rect.bottom <= 0:
                self.missiles.remove(missile)

        # Check for any missiles that have hit alien ships.
        # If collisions detected, remove both alien ship and missile.
        collisions = pygame.sprite.groupcollide(self.missiles, self.aliens, True, True)

    def _create_alien_fleet(self):
        """ Create a fleet of alien ships. """
        # Create an alien to obtain dimensions
        alien = Alien(self)
        alien_ship_width, alien_ship_height = alien.rect.size

        # Calculate available x space for the number of alien ship objects
        available_space_x = self.settings.screen_width - (2 * alien_ship_width)
        number_aliens_x = available_space_x // (2 * alien_ship_width)

        # Calculate available y space for number of alien ship rows
        spaceship_height = self.spaceship.image_rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_ship_height) - spaceship_height)
        number_rows = available_space_y // (2 * alien_ship_height)

        # Create a fleet of alien ships
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, alien_ship_width, row_number)

    def _create_alien(self, alien_number, alien_ship_width, row_number):
        """ Create an alien ship and place it in the row. """
        alien = Alien(self)
        alien.x = alien_ship_width + 2 * alien_ship_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_alien_edges(self):
        """ Respond when alien fleet has reached the edge of the screen. """
        for alien in self.aliens.sprites():
            if alien.check_screen_edge():
                self._change_alien_direction()
                break

    def _change_alien_direction(self):
        """ Drop the alien ships down and change opposite direction. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        # Toggle between right/left; 1 (right) or -1 (left)
        self.settings.alien_direction *= -1

    def _update_aliens(self):
        """ Update alien ships on screen """
        self._check_alien_edges()
        self.aliens.update()

    def _update_screen(self):
        """ Update images on screen and flip to the new screen. """
        self.screen.fill(self.settings.BACKGROUND_COLOR)
        self.spaceship.blitme()

        for missile in self.missiles.sprites():
            missile.draw_missile()

        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__ == '__main__':
    # Launch the game.
    space_invaders = SpaceInvaders()
    space_invaders.run_game()
