import pygame


class SoundEffects:
    """ A class to manage the sound effects of the game. """

    def __init__(self, game_stats):
        """ Initialise class attributes. """

        # Create a handle to game stats for access to game_active flag.
        self.game_stats = game_stats

        # Sound files
        self.missile_sound = 'sounds/missile.wav'
        self.explosion_sound = 'sounds/explosion.wav'
        self.alien_hit = 'sounds/alien_hit.wav'
        self.background_sound = 'sounds/background.ogg'

    def play_sound(self, sound_effect):
        """ Check if game is active & play the required sound effect. """

        if self.game_stats.game_active:
            if sound_effect == 'missile':
                sound_file = self.missile_sound
            elif sound_effect == 'explosion':
                sound_file = self.explosion_sound
            elif sound_effect == 'alien_hit':
                sound_file = self.alien_hit

            pygame.mixer.Sound(sound_file).play()

    def start_ambient_sound(self):
        """ Start playing the games background sound on a continuous loop. """
        pygame.mixer.Sound("sounds/background.ogg").play(-1)