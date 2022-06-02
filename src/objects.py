import pygame
import os
import math
import random


class Lander(pygame.sprite.Sprite):
    def __init__(self, settings):
        pygame.sprite.Sprite.__init__(self)

        # Load lander image and keep a copy of the original to be used in transformation operations.
        self.image_or = pygame.image.load(os.path.join("resources", "lander.png"))
        self.image = self.image_or

        # Create a mask used for collision detection.
        self.mask = pygame.mask.from_surface(self.image)

        # Get the lander's rectangle and position it at the top of the screen.
        self.rect = self.image_or.get_rect()
        self.rect.center = (settings.screen_width / 2, self.rect.height / 2)

        # Initialise variables.
        self.angle = 0
        self.velocity_y = random.random()
        self.velocity_x = random.uniform(-1, 1)
        self.fuel = 1000
        self.damage = 0
        self.has_landed = False
        self.has_crashed = False

        # Create the thruster which will be displayed under the lander.
        self.thruster = Thruster(self.rect.midbottom)

    # This function is called once per frame and is responsible for adjusting the lander's position
    # as well as detecting crashes at the bottom of the screen.
    def move(self, settings):

        # Adjust position according to current speed values. Since rect x and y coordinates can be adjusted only by
        # integer increments and the starting velocity for x axis is a float, we use the function round() to provide
        # a more even adjustment with respect to the default "flooring" performed by the mere addition between
        # rect coordinates and floats.
        self.rect.y += round(self.velocity_y)
        self.rect.x += round(self.velocity_x)

        # Crash the lander at the bottom of the screen.
        if self.rect.bottom > settings.screen_height:
            self.rect.bottom = settings.screen_height
            self.damage = 100
            self.has_crashed = True

        # Prevent the lander from flying off the top.
        elif self.rect.top < 0:
            self.rect.top = 0

        # Wrap around the right and left side.
        if self.rect.centerx > settings.screen_width:
            self.rect.centerx = 0
        elif self.rect.centerx < 0:
            self.rect.centerx = settings.screen_width

    # Rotates the lander's and the thruster's image towards the given direction.
    def turn(self, direction):

        # Adjust angle.
        if direction == "Right":
            self.angle -= 1
        elif direction == "Left":
            self.angle += 1

        # Allow a maximum rotation of 90 degrees.
        if self.angle > 90:
            self.angle = 90
        elif self.angle < -90:
            self.angle = -90

        # Transform the lander's image.
        self.image = pygame.transform.rotate(self.image_or, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Transform the thruster's image.
        self.thruster.image = pygame.transform.rotate(self.thruster.image_or, self.angle)

    # Fires the thruster to accelerate the lander if there is enough fuel available.
    def accelerate(self):
        if self.fuel >= 5:
            # This flag is used for deciding whether to draw the thruster or not.
            self.thruster.is_active = True

            self.velocity_x += 1 * 0.33 * math.sin(math.radians(-self.angle))
            self.velocity_y -= 1 * 0.33 * math.cos(math.radians(self.angle))
            self.fuel -= 5
        else:
            self.thruster.is_active = False

    # This is the main update function of the lander and is called once per frame.
    def update(self, settings):

        # Increase falling speed.
        self.velocity_y += 0.1

        self.move(settings)
        self.thruster.update(self.rect.midbottom, self.angle)

    # Draws lander and thruster.
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.thruster.draw(screen)


class Thruster(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)

        # Load lander image and keep a copy of the original to be used in transformation operations.
        self.image_or = pygame.image.load(os.path.join("resources", "thrust.png"))
        self.image = self.image_or

        # Get the lander's rectangle and position it just below the lander.
        self.rect = self.image_or.get_rect()
        self.rect.center = pos

        # This flag is used for distinguishing whether to draw the thruster or not.
        self.is_active = False

    # This function is called once per frame and updates the thruster's position to keep it just below the lander.
    def update(self, lander_pos, lander_angle):
        self.rect.center = lander_pos
        thruster_offset = -lander_angle * 0.5
        self.rect.centerx -= thruster_offset
        self.rect.centery -= abs(thruster_offset)

    # Draws the thruster if it is active.
    def draw(self, screen):
        if self.is_active:
            screen.blit(self.image, self.rect)


class LandingPad(pygame.sprite.Sprite):
    def __init__(self, settings, pos):

        # For each one of the 3 landing pads there are 4 possible spawn locations.
        spawn_points = [(975 * settings.screen_width / 1200, 699 * settings.screen_height / 750),
                        (1122 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (1022 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (913 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (743 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (514 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (642 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (425 * settings.screen_width / 1200, 617 * settings.screen_height / 750),
                        (245 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (167 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (82 * settings.screen_width / 1200, 750 * settings.screen_height / 750),
                        (254 * settings.screen_width / 1200, 436 * settings.screen_height / 750)]

        # Load a tall or normal image for a landing pad with a 50% chance.
        if random.randint(1, 100) < 51:
            self.isTall = False
        else:
            self.isTall = True
        pygame.sprite.Sprite.__init__(self)
        if self.isTall:
            self.image = pygame.image.load(os.path.join("resources", "landingPads", "pad_tall.png"))
        else:
            self.image = pygame.image.load(os.path.join("resources", "landingPads", "pad.png"))

        # Get its rectangle and mask used for collision / landing detection.
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Randomly select one of the 4 spawning points for the first, second and third landing pad.
        result = random.randint(pos * 4, pos * 4 + 3)
        self.rect.centery = (spawn_points[result][1] - (self.rect.height / 2))
        self.rect.centerx = (spawn_points[result][0])


# Parent class of obstacles (static) and meteors that can damage the lander upon impact.
class Hazard(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        pygame.sprite.Sprite.__init__(self)

        # Get image mask used for collision detection.
        self.mask = pygame.mask.from_surface(image)

        # Get image rectangle and position it at the given coordinates.
        self.rect = image.get_rect()
        self.rect.center = pos

        # This flag is set at the first frame when the lander collides with the item
        # in order to prevent the collisions detected in the following frames from damaging repeatedly the lander.
        # The flag is cleared when the lander stops "touching" the item
        # so that a subsequent collision with the same item can damage it again.
        self.is_touching = False

    # Overridden in class Meteor, class Obstacle.
    def update(self, settings):
        return


# Meteors are moving sprites created by the mission at a given starting position.
class Meteor(Hazard):
    def __init__(self, pos, spawns_from):
        self.image = pygame.image.load(os.path.join("resources", "meteors", "spaceMeteors_00%d.png" % random.randint(1, 4)))
        Hazard.__init__(self, pos, self.image)

        # Spawn location with respect to the screen sides.
        self.spawns_from = spawns_from

        self.damage_caused = 25

    # Main update function of the Meteor, responsible for moving and despawning them.
    def update(self, settings):

        # Move the meteor closer to the ground and to the left or right of the screen depending on the spawn location.
        if self.spawns_from == "Right":
            self.rect.centerx -= 13
        else:
            self.rect.centerx += 13
        self.rect.centery += 13

        # Despawn the meteor when it gets passed the screen bottom and the appropriate screen side.
        if self.spawns_from == "Left":
            if self.rect.topleft[0] > settings.screen_width or self.rect.topleft[1] > settings.screen_height:
                self.kill()
        else:
            if self.rect.topright[0] < 0 or self.rect.topright[1] > settings.screen_height:
                self.kill()


# Obstacles are static (immovable) sprites created by the mission at a given position.
class Obstacle(Hazard):
    def __init__(self, pos, image):
        self.image = pygame.image.load(os.path.join("resources", "obstacles",  image + ".png"))
        Hazard.__init__(self, pos, self.image)
        self.damage_caused = 10


class Avatar:
    def __init__(self, settings, lives):
        self.image = pygame.image.load(os.path.join("resources", "lander.png"))
        self.image_rect = self.image.get_rect(center=(settings.screen_width - 145, 50))
        self.avatar_font = pygame.font.SysFont('Comic Sans MS', 40)
        self.avatar_text = self.avatar_font.render(" X %d" % lives, True, (255, 255, 255))
        self.avatar_text_rect = self.avatar_text.get_rect(center=(settings.screen_width - 80, 50))

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)
        screen.blit(self.avatar_text, self.avatar_text_rect)
