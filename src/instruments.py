import pygame
import os
import random
from visuals import Breather, RedGreenMixer


# This class is responsible for managing the various data displayed on the instruments panel of the screen, as well as
# handling the normal operation and malfunctions of the lander controls.
class Instruments:
    def __init__(self, lander, settings, score):

        # Load the background for the instruments panel.
        self.bg = pygame.image.load(os.path.join("resources", "instruments.png"))
        self.bg = pygame.transform.smoothscale(self.bg, (350, 115))

        # Create fonts for the instruments panel.
        self.my_instr_font = pygame.font.SysFont('Arial', 20)
        self.my_alert_font = pygame.font.SysFont('Arial', 30, bold=True)

        # Create Breather and Mixer objects to handle the multicolored font of fuel and alert display.
        self.breather = Breather("fast")
        self.mixer = RedGreenMixer()

        # Initialise instrument panel values.
        self.time = 0
        self.time_text = self.my_instr_font.render("{0:5.1f}".format(round(self.time / 1000, 1)),
                                                   True, (200, 200, 200))
        self.fuel = lander.fuel
        self.fuel_text = self.my_instr_font.render("{0:5d}".format(lander.fuel, 2),
                                                   True, (self.mixer.red_fuel, self.mixer.green_fuel, 0))
        self.damage = lander.damage
        self.damage_text = self.my_instr_font.render("{0:5d}".format(lander.damage, 2),
                                                     True, (self.mixer.red_damage, self.mixer.green_damage, 0))
        self.altitude_text = self.my_instr_font.render("{0:5.0f}".format((settings.screen_height
                                                                          - lander.rect.bottom)
                                                                         * (1000 / (settings.screen_height
                                                                                    - lander.rect.height))),
                                                       True, (200, 200, 200))
        self.velocity_x_text = self.my_instr_font.render("{0:5.1f}".format(round(lander.velocity_x, 2)),
                                                         True, (200, 200, 200))
        self.velocity_y_text = self.my_instr_font.render("{0:5.1f}".format(round(lander.velocity_y, 2)),
                                                         True, (200, 200, 200))
        self.score = score
        self.score_text = self.my_instr_font.render("{0:5.0f}".format(self.score),
                                                    True, (255, 255, 0))
        self.alert_text = self.my_alert_font.render("* ALERT! *", True, (self.breather.color_value, 0, 0))

        # This variable shows which of the controls is malfunctioning at the current moment.
        self.failure = "None"

        # The time when the last malfunction occurred.
        self.failure_time = 0

    # Main update function of the Instruments class. Called once per frame, it randomly generates control failures,
    # as well as updates the various data displayed on the panel.
    def update(self, clock, lander, settings, difficulty_level):
        # Update the time passed.
        self.time += clock.get_time()

        # Set all controls as malfunctioning if the lander has sustained 100% damage.
        if lander.damage == 100:
            self.failure = "Total"
            lander.thruster.is_active = False

        # If no control is malfunctioning at the current moment, generate a random control failure
        # with a chance which is dependant on the current mission difficulty level
        # and store the moment at which it occurred.
        if self.failure == "None":
            unlucky_factor = random.randint(1, 2400 - 160 * difficulty_level)
            if unlucky_factor == 1:
                self.failure = "Left"
            elif unlucky_factor == 2:
                self.failure = "Right"
            if unlucky_factor <= 2:
                self.failure_time = self.time

        # If a single control was malfunctioning, fix it if 2 seconds have passed.
        elif self.failure != "Total":
            if self.time - self.failure_time > 2000:
                self.failure = "None"

        # Update instruments panel data.
        self.time_text = self.my_instr_font.render("{0:5.1f}".format(round(self.time / 1000, 1)),
                                                   True, (200, 200, 200))
        self.fuel = lander.fuel
        self.mixer.mix_fuel(self.fuel)
        self.fuel_text = self.my_instr_font.render("{0:5d}".format(lander.fuel, 2),
                                                   True, (self.mixer.red_fuel, self.mixer.green_fuel, 0))
        self.damage = lander.damage
        self.mixer.mix_damage(self.damage)
        self.damage_text = self.my_instr_font.render("{0:5d}".format(lander.damage, 2),
                                                     True, (self.mixer.red_damage, self.mixer.green_damage, 0))
        self.altitude_text = self.my_instr_font.render("{0:5.0f}".format((settings.screen_height - lander.rect.bottom)
                                                                         * (1000 / (settings.screen_height
                                                                                    - lander.rect.height))),
                                                       True, (200, 200, 200))
        self.velocity_x_text = self.my_instr_font.render("{0:5.1f}".format(round(lander.velocity_x, 2)),
                                                         True, (200, 200, 200))
        self.velocity_y_text = self.my_instr_font.render("{0:5.1f}".format(round(lander.velocity_y, 2)),
                                                         True, (200, 200, 200))
        if self.failure != "None":
            self.breather.breathe()
            self.alert_text = self.my_alert_font.render("* ALERT! *", True, (self.breather.color_value, 0, 0))

    # Draws instruments panel data on the screen
    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        screen.blit(self.time_text, (100, 10))
        screen.blit(self.fuel_text, (100, 32))
        screen.blit(self.damage_text, (100, 54))
        screen.blit(self.score_text, (100, 81))
        screen.blit(self.altitude_text, (280, 10))
        screen.blit(self.velocity_x_text, (280, 32))
        screen.blit(self.velocity_y_text, (280, 54))
        if self.failure != "None":
            screen.blit(self.alert_text, (172, 77))

    # Activates left turn control if functional
    def engage_left_control(self, lander):
        if self.failure != "Left" and self.failure != "Total":
            lander.turn("Left")

    # Activates right turn control if functional
    def engage_right_control(self, lander):
        if self.failure != "Right" and self.failure != "Total":
            lander.turn("Right")

    # Activates thruster control if functional
    def engage_thrust_control(self, lander):
        if self.failure != "Thrust" and self.failure != "Total":
            lander.accelerate()
