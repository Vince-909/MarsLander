import pygame
from settings import Settings
from screens import MenuScreen


# Main game class.
class MarsLander:
    def __init__(self):

        # Initialise the pygame module.
        pygame.init()

        # Create a Settings object to hold the screen dimensions, starting number of lives and desired FPS.
        self.settings = Settings()

        # Create a display screen.
        if self.settings.fullscreen_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1200, 750))
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.settings.screen_width = screen_width
        self.settings.screen_height = screen_height

        # Initialise pygame fonts.
        pygame.font.init()

        # Create a menu (pre-game) screen as the first active screen.
        self.active_screen = MenuScreen(self.settings, False, 0)

    # Main game loop.
    def play(self):
        while True:

            # Progress the active screen.
            self.active_screen.play(self.settings)

            # Draw the active screen.
            self.active_screen.draw(self.screen, self.settings)

            # Decide whether to switch the currently active screen or keep at it.
            self.active_screen = self.active_screen.select_next_active_screen(self.settings)

            # Flip the display.
            pygame.display.update()


# Initialise the game and enjoy!
mars_lander = MarsLander()
mars_lander.play()
