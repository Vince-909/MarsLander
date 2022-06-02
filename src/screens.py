import sys
import os
import pygame
import random
from visuals import Breather
from mission import Mission


# Parent class of menu and game play screens.
class Screen:
    def __init__(self, settings):
        # Load the screens's background image.
        self.bg = pygame.image.load(os.path.join("resources", "mars_background.png"))
        self.bg = pygame.transform.smoothscale(self.bg, (settings.screen_width, settings.screen_height))
        return

    # Overridden in MenuScreen/GamePlayScreen classes.
    def play(self, settings):
        return

    # Overridden in MenuScreen/GamePlayScreen classes.
    def draw(self, screen, settings):
        return

    # Overridden in MenuScreen/GamePlayScreen classes.
    def select_next_active_screen(self):
        return


# This class represents the function and visualisation of the pre-game and post-game menu screens.
class MenuScreen(Screen):
    def __init__(self, settings, game_over, final_score):

        # Call parent class init() to load the background image.
        Screen.__init__(self, settings)

        # Flag used to distinguish between pre-game and post-game menus.
        self.game_over = game_over

        # Load a lander image to be used as a selection cursor for the menu options.
        self.cursor = pygame.image.load(os.path.join("resources", "lander.png"))

        # Initialise menu text fields and fonts.
        self.selected = "left_choice"
        if self.game_over:
            self.title = "Game Over!"
            self.left_choice = "Play Again"
            self.right_choice = "Quit"
        else:
            self.title = "Mars Lander"
            self.left_choice = "New Game"
            self.right_choice = "Continue"
        self.my_error_font = pygame.font.SysFont("Arial", 25)
        self.my_menu_font = pygame.font.SysFont("Comic Sans MS", 40)
        self.my_title_font = pygame.font.SysFont("Comic Sans MS", 50, bold=True)
        self.my_instructions_font = pygame.font.SysFont("Comic Sans MS", 20, bold=True, italic=True)
        self.my_credits_font = pygame.font.SysFont("Comic Sans MS", 30, bold=True, italic=True)
        self.title_text = self.my_title_font.render(self.title, True, (255, 255, 255))
        self.title_text_rect = self.title_text.get_rect(center=(settings.screen_width / 2,
                                                                settings.screen_height / 4))
        self.left_choice_text = self.my_menu_font.render(self.left_choice, True, (255, 255, 255))
        self.left_choice_text_rect = self.left_choice_text.get_rect(center=(settings.screen_width / 2 - 150,
                                                                            settings.screen_height * 3 / 5))
        self.left_choice_text_color = 0
        self.right_choice_text = self.my_menu_font.render(self.right_choice, True, (255, 255, 255))
        self.right_choice_text_rect = self.right_choice_text.get_rect(center=(settings.screen_width / 2 + 150,
                                                                              settings.screen_height * 3 / 5))
        self.right_choice_text_color = 0
        self.final_score = final_score
        self.final_score_text = self.my_menu_font.render("Score: {0:5d}".format(self.final_score), True, (255, 255, 0))
        self.final_score_text_rect = self.final_score_text.get_rect(center=(settings.screen_width / 2,
                                                                            settings.screen_height * 17 / 40))
        self.instructions_text = ["How to play:",
                                  "Carefully descend upon one of the three landing pads while"
                                  " avoiding meteors and obstacles.", "Use [LEFT] and [RIGHT] arrow keys to rotate the"
                                                                      " lander and [SPACE] to fire the thruster.",
                                  "[ESC] quits the game.", "Good Luck!"]
        self.multi_text = []
        for line in self.instructions_text:
            self.multi_text.append(self.my_instructions_font.render(line, True, (50, 50, 50)))
        self.error_text = self.my_error_font.render("No saved game found.", True, (255, 0, 0))
        self.error_text_rect = self.error_text.get_rect(center=(settings.screen_width / 2 + 150,
                                                                settings.screen_height * 3 / 5 + 50))
        self.credits_text = self.my_credits_font.render("Developed by Vince", True, (50, 50, 50))
        self.credits_text_rect = self.credits_text.get_rect(center=(settings.screen_width / 2,
                                                                            settings.screen_height - 30))

        # Get the cursor's rectangle and position it atop the left menu choice.
        self.cursor_rect = self.cursor.get_rect()
        self.cursor_rect.center = (self.left_choice_text_rect.centerx, self.left_choice_text_rect.y - 20)

        # Flag indicating when the load game error message should be visible.
        self.print_error = False

        # This flag indicates when the menu screen should stop rendering and give its place to the game play screen.
        self.game_starts = False

        # Create a Breather object to handle the multicolored font of the highlighted menu entry.
        self.breather = Breather("slow")

        self.starting_score = 0
        self.starting_level = 1
        self.starting_lives = settings.lives

    # Called for each frame from the main game loop, implements the pre-game and post-game menus.
    def play(self, settings):

        # Highlight the default (left) selected menu entry.
        self.breather.breathe()
        if self.selected == "left_choice":
            self.left_choice_text_color = self.breather.color_value
            self.right_choice_text_color = 255
        elif self.selected == "right_choice":
            self.right_choice_text_color = self.breather.color_value
            self.left_choice_text_color = 255
        self.left_choice_text = self.my_menu_font.render(self.left_choice, True,
                                                         (self.left_choice_text_color, self.left_choice_text_color,
                                                          self.left_choice_text_color))
        self.right_choice_text = self.my_menu_font.render(self.right_choice, True, (self.right_choice_text_color,
                                                                                    self.right_choice_text_color,
                                                                                    self.right_choice_text_color))

        # Handle user keyboard input.
        for event in pygame.event.get():

            # Quit the game.
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:

                # Quit the game.
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

                # Move the cursor to select another menu entry.
                elif event.key == pygame.K_LEFT and self.selected == "right_choice":
                    self.move_cursor()
                elif event.key == pygame.K_RIGHT and self.selected == "left_choice":
                    self.move_cursor()

                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:

                        # Signal the start of a game if the menu entry to the left is selected.
                        if self.selected == "left_choice":
                            self.game_starts = True

                        # If the menu entry to the right is selected, the post-game menu quits the game
                        # while the pre-game menu attempts to start a saved game.
                        else:
                            if self.game_over:
                                sys.exit()
                            else:
                                if self.load_game():
                                    self.game_starts = True
                                else:
                                    self.print_error = True

    # Called for each frame from the main game loop, renders the pre-game and post-game menus.
    def draw(self, screen, settings):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.title_text, self.title_text_rect)
        if self.game_over:
            screen.blit(self.final_score_text, self.final_score_text_rect)
            screen.blit(self.credits_text, self.credits_text_rect)
        else:
            for line in range(len(self.multi_text)):
                screen.blit(self.multi_text[line], (settings.screen_width / 2 -
                                                    self.multi_text[line].get_rect().width / 2,
                                                    (settings.screen_height / 4 + (line * 20) + (10 * line) + 50)))
        screen.blit(self.left_choice_text, self.left_choice_text_rect)
        screen.blit(self.right_choice_text, self.right_choice_text_rect)
        screen.blit(self.cursor, self.cursor_rect)
        if self.print_error:
            screen.blit(self.error_text, self.error_text_rect)

    # Called for each frame from the main game loop, this function handles the transition
    # from the menu screens to the game play screen.
    def select_next_active_screen(self, settings):

        # Exit the menu and start the game if either "New Game", "Continue" or "Play Again" was activated.
        if self.game_starts:
            pygame.event.clear()
            return GamePlayScreen(settings, self.starting_level, self.starting_score, self.starting_lives)
        else:
            return self

    # Toggles cursor position.
    def move_cursor(self):
        self.print_error = False
        if self.selected == "left_choice":
            self.selected = "right_choice"
            self.cursor_rect.center = (self.right_choice_text_rect.centerx, self.right_choice_text_rect.y - 20)
        else:
            self.selected = "left_choice"
            self.cursor_rect.center = (self.left_choice_text_rect.centerx, self.left_choice_text_rect.y - 20)

    # Attempts to load a previously unfinished game.
    def load_game(self):
        if not os.path.isfile("saved_game.save"):
            return False
        save = open("saved_game.save", "r")
        data = save.readlines()
        if not data:
            return False
        for line in data:
            nums = line.split()
        self.starting_level = int(nums[0])
        self.starting_score = int(nums[1])
        self.starting_lives = int(nums[2])
        save.close()
        return True


# This class represents the progression and visualisation of the actual game play.
class GamePlayScreen(Screen):
    def __init__(self, settings, level, score, lives):

        # Call parent class init() to load the background image.
        Screen.__init__(self, settings)

        # Initialise text fields and fonts.
        self.my_message_font = pygame.font.SysFont('Comic Sans MS', 40)
        self.my_message_font_small = pygame.font.SysFont('Arial', 20)
        self.crash_message = self.my_message_font.render("You Have Crashed !!!", True, (255, 0, 0))
        self.crash_message_rect = self.crash_message.get_rect(center=(settings.screen_width / 2,
                                                                      settings.screen_height / 2))
        self.landing_message = self.my_message_font.render("Landing Successful !", True, (0, 255, 0))
        self.landing_message_rect = self.landing_message.get_rect(center=(settings.screen_width / 2,
                                                                          settings.screen_height / 2))
        self.press_key_message = self.my_message_font_small.render("press any key to continue", True, (0, 0, 0))
        self.press_key_message_rect = self.press_key_message.get_rect(center=(settings.screen_width / 2,
                                                                      settings.screen_height / 2 + 50))

        self.score = score
        self.level = level
        self.lives = lives

        # Create a new mission at the given level and with the given starting score.
        self.mission = Mission(settings, self.score, self.level, self.lives)

    # Called for each frame from the main game loop, implements the actual game play.
    def play(self, settings):

        # Check if the mission has ended.
        if self.mission.lander.has_crashed or self.mission.lander.has_landed:

            # Disable key repeat.
            pygame.key.set_repeat(0, 0)

            # Decrease lives if the mission ended with a crash.
            if self.mission.lander.has_crashed:
                self.lives -= 1

            # If the mission ended with a landing increase player score and level of next mission.
            else:
                self.score += 50
                self.level += 1

            # Save the game's state (score, level and lives) if it is passed the first level.
            if not (self.mission.level == 1 and self.mission.lander.has_crashed):
                self.save_game()

            self.press_any_key()

            # End the game and delete checkpoint data if lives are exhausted.
            if self.lives == 0:
                self.delete_saved_game()
                return

            # Create the next mission.
            self.mission = Mission(settings, self.score, self.level, self.lives)

        # Force the desired FPS.
        self.mission.clock.tick_busy_loop(settings.FPS)

        # Handle user keyboard input.
        for event in pygame.event.get():

            # Quit the game.
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()

            # Attempt to navigate to the left.
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.mission.instruments.engage_left_control(self.mission.lander)

            # Attempt to navigate to the right.
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.mission.instruments.engage_right_control(self.mission.lander)

            # Attempt to fire the thruster.
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.mission.instruments.engage_thrust_control(self.mission.lander)

            # Disable the thruster's visual when space is released.
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.mission.lander.thruster.is_active = False

        # If not already active, create a meteor storm with a chance which increases as level difficulty increases.
        if (not self.mission.storm_is_active) and (self.mission.last_storm_end < self.mission.instruments.time - 2000):
            if random.randint(1, 600 - 55 * self.mission.difficulty_level) == 1:
                self.mission.create_meteor_storm(settings)

        # Update sprites (meteors/obstacles)
        self.mission.lander.update(settings)
        self.mission.hazards.update(settings)

        # Note the time at which the last meteor storm ended.
        if self.mission.storm_is_active and len(self.mission.hazards) == 5:
            self.mission.last_storm_end = self.mission.clock.get_time()
            self.mission.storm_is_active = False

        # Check for collisions between the lander and obstacles/meteors.
        self.mission.check_hits()

        # Check for collision (landing or crash) between the lander and the landing pads.
        self.mission.check_landing()

        # Update the data visible on the instruments panel.
        self.mission.instruments.update(self.mission.clock, self.mission.lander, settings,
                                        self.mission.difficulty_level)

    # Called for each frame from the main game loop, renders the in-game objects.
    def draw(self, screen, settings):
        screen.blit(self.bg, (0, 0))
        self.mission.instruments.draw(screen)
        self.mission.avatar.draw(screen)
        self.mission.lander.draw(screen)
        self.mission.landing_sprites.draw(screen)
        self.mission.hazards.draw(screen)
        if self.mission.lander.has_crashed:
            screen.blit(self.crash_message, self.crash_message_rect)
            screen.blit(self.press_key_message, self.press_key_message_rect)
        elif self.mission.lander.has_landed:
            screen.blit(self.landing_message, self.landing_message_rect)
            screen.blit(self.press_key_message, self.press_key_message_rect)

    # Called for each frame from the main game loop, this function handles the transition
    # from the game play screen to the menu (post-game) screen.
    def select_next_active_screen(self, settings):

        # End the game and enter the post-game menu if no more lives remain after a crash.
        if self.mission.lander.has_crashed and self.lives == 0:
            pygame.event.clear()
            return MenuScreen(settings, True, self.score)
        else:
            return self

    # This function pauses the game until the user presses any key.
    def press_any_key(self):
        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

    # Saves the current game status (mission level, score and remaining lives) to a file.
    def save_game(self):
        save = open("saved_game.save", "w")
        save.write("%d %d %d" % (self.level, self.score, self.lives))
        save.close()

    # Deletes the saved game data.
    def delete_saved_game(self):
        if os.path.isfile("saved_game.save"):
            os.remove("saved_game.save")
