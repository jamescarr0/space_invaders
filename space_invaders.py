import sys
import pygame

from time import sleep

from settings import Settings
from spaceship import Spaceship
from spaceship_missile import SpaceshipMissile
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound_effects import SoundEffects


class SpaceInvaders:
    """ General class to manage game assets and behaviour. """

    def __init__(self):
        """ Initialise and create objects. """
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(self.settings.WINDOW_TITLE)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width, self.settings.screen_height = pygame.display.get_surface().get_size()

        # Load background image and scale to screen size.
        self.bg = pygame.image.load('images/milky_way.jpg').convert()
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_width, self.settings.screen_height))

        self.spaceship = Spaceship(self)
        self.missiles = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_alien_fleet()

        # Create the start game button.
        self.play_button = Button(self, "Start Game")

        # Create scoreboard and instance to store game statistics
        self.game_stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Create a sound instance to play sounds.
        self.sfx = SoundEffects(self.game_stats)

    def run_game(self):
        """ Run game - Begin main loop for game. """

        # Start the games background sound.
        self.sfx.start_ambient_sound()

        while True:
            fps = self.clock.get_fps()
            self._check_events()

            if self.game_stats.game_active:
                self.spaceship.move()
                self._update_missiles()
                self._update_aliens()
                self.scoreboard.prepare_frames_per_second(fps)

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_events(self):
        """ Watch for, and respond to keyboard and mouse events. """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Terminate via window closure.
                # Persist high score before terminating game.
                self._persist_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button_pressed(mouse_position)

    def _check_play_button_pressed(self, mouse_position):
        """ Begin game when player clicks the start/play button. """

        if self.play_button.rect.collidepoint(mouse_position) and not self.game_stats.game_active:
            # Reset game stats and dynamic game settings.
            self.game_stats.reset_stats()
            self.game_stats.game_active = True
            self.settings.initialise_dynamic_settings()

            # Reset the scoreboard
            self.scoreboard.prepare_scoreboard_images()

            # Reset aliens and missiles.
            self.aliens.empty()
            self.missiles.empty()

            # Create a new fleet and aliens and center players spaceship.
            self._create_alien_fleet()
            self.spaceship.respawn()

            # Hide the mouse cursor when game is active
            pygame.mouse.set_visible(False)

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
            # Persist the high score before terminating game.
            self._persist_high_score()
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
        """ Create a new missile, add it to the missiles sprite group and play the missile sound effects. """
        if len(self.missiles) < self.settings.missile_count:
            new_missile = SpaceshipMissile(self)
            self.missiles.add(new_missile)

            # Play missile sound effect.
            self.sfx.play_sound('missile')

    def _update_missiles(self):
        """ Update missile positions and remove missiles that are off the screen. """
        self.missiles.update()
        for missile in self.missiles.copy():
            if missile.rect.bottom <= 0:
                self.missiles.remove(missile)

        self._check_missile_collisions()

    def _check_missile_collisions(self):
        """ Respond to missile-alien collisions. """
        # Remove missiles and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.missiles, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                # Add points to the game score for every alien that has been hit with a missile including multiple
                # strikes with one missile.
                # Play sound effect for every alien hit.
                self.game_stats.score += self.settings.alien_points * len(aliens)
                self.sfx.play_sound('explosion')

            # Update the current score and check for a new high score.
            self._update_scoreboard()

        # An empty group evaluates to False. Level up!
        if not self.aliens:
            self._level_up()

    def _update_scoreboard(self):
        """ Update the game scores. """
        self.scoreboard.prepare_game_score()
        self.scoreboard.check_high_score()

    def _create_alien(self, alien_number, alien_ship_width, row_number):
        """ Create an alien ship and place it in the row. """
        alien = Alien(self)
        alien.x = alien_ship_width + 2 * alien_ship_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height + 2 * alien.rect.height * row_number) + 20
        self.aliens.add(alien)

    def _create_alien_fleet(self):
        """ Create a fleet of alien ships. """
        # Create an alien to obtain dimensions
        alien = Alien(self)
        alien_ship_width, alien_ship_height = alien.rect.size
        number_aliens_x, number_rows = self._calculate_space_for_aliens(alien_ship_height, alien_ship_width)

        # Create a fleet of alien ships
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, alien_ship_width, row_number)

    def _calculate_space_for_aliens(self, alien_ship_height, alien_ship_width):
        """ Calculate available x and y space for the number of alien ships and the number of rows of ships. """

        # Calculate available x space for the number of alien ship objects
        available_space_x = self.settings.screen_width - (2 * alien_ship_width)
        number_aliens_x = available_space_x // (2 * alien_ship_width)

        # Calculate available y space for number of alien ship rows
        spaceship_height = self.spaceship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_ship_height) - spaceship_height)
        number_rows = available_space_y // (2 * alien_ship_height)
        return number_aliens_x, number_rows

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

    def _check_aliens_bottom(self):
        """ Respond to aliens reaching the bottom of the screen. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Same action as if the spaceship has been hit.
                self._spaceship_hit()
                break

    def _spaceship_hit(self):
        """ Respond to spaceship colliding with an alien """
        # Play alien striking spaceship sound.
        self.sfx.play_sound('alien_hit')

        if self.game_stats.ships_remaining > 1:
            # Decrement a life.
            self.game_stats.ships_remaining -= 1
            self.scoreboard.prepare_lives()

            # Remove remaining aliens and missiles
            self.aliens.empty()
            self.missiles.empty()

            # Create a new fleet of aliens and center the spaceship.
            self._create_alien_fleet()
            self.spaceship.respawn()

            # Briefly Pause so player can regroup before new fleet arrives.
            sleep(2.0)
        else:
            self.game_stats.ships_remaining -= 1
            self.scoreboard.prepare_lives()
            self.game_stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """ Update alien ships on screen """
        self._check_alien_edges()
        self.aliens.update()

        # Check for aliens hitting spaceship.
        if pygame.sprite.spritecollide(self.spaceship, self.aliens, False):
            self._spaceship_hit()

        # Check for aliens reaching the bottom of the screen.
        self._check_aliens_bottom()

    def _level_up(self):
        """ Level up game play. """
        # Destroy existing missiles and create a new fleet of alien ships.
        self.missiles.empty()
        self._create_alien_fleet()
        self.settings.increase_speed()

        # Increment Level
        self.game_stats.level += 1
        self.scoreboard.prepare_level()

    def _persist_high_score(self):
        """ Persist the high score to file. """
        with open(self.settings.high_score_file, 'w') as high_score_file:
            high_score_file.write(str(self.game_stats.high_score))

    def _update_screen(self):
        """ Update images on screen and flip the new screen. """
        self.screen.blit(self.bg, self.screen.get_rect())
        self.spaceship.blitme()

        for missile in self.missiles.sprites():
            missile.draw_missile()

        self.aliens.draw(self.screen)

        # Draw the scoreboard information.
        self.scoreboard.show_scoreboard()

        # Draw start game button if the game state is inactive.
        if not self.game_stats.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()
