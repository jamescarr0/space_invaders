import pygame.font


class Button:

    def __init__(self, game, message):
        """ Initialise button attributes """
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 300, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('support_files/retro_font.ttf', 22)

        # Create the buttons rect object and position central to screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Render message
        self._render_message(message)

    def _render_message(self, message):
        """ Turn message into a rendered image and center text on the button. """
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        """ Draw a button to screen, then draw the message. """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
