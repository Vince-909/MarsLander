import pygame
import random
import math
from objects import Lander, LandingPad, Meteor, Obstacle, Avatar
from instruments import Instruments


class Mission:
    def __init__(self, settings, score, level, lives):

        # Set keys to repeat when held down.
        pygame.key.set_repeat(25, 25)

        # Initialise mission level and difficulty, with difficulty capping at level 10.
        self.level = level
        self.difficulty_level = level
        if self.difficulty_level > 10:
            self.difficulty_level = 10

        # Create a Clock object to help keep track of time.
        self.clock = pygame.time.Clock()

        # Create a lander avatar to display remaining lives.
        self.avatar = Avatar(settings, lives)

        # Create the lander.
        self.lander = Lander(settings)

        # Create the instrument panel.
        self.instruments = Instruments(self.lander, settings, score)

        # Create a sprite group and add 3 landing pads.
        self.landing_sprites = pygame.sprite.Group()
        for x in range(3):
            self.landing_sprites.add(LandingPad(settings, x))

        # Create a sprite group to hold obstacles and meteors.
        self.hazards = pygame.sprite.Group()

        # Create and initialise the static obstacles for the mission.
        self.create_obstacles(settings)

        # Flag that shows that a meteor storm is taking place.
        self.storm_is_active = False
        self.last_storm_end = 0

    # This function checks if the lander has made some kind of contact with any landing pad.
    def check_landing(self):

        # Check for collision with a landing pad.
        touched_landing_pad = pygame.sprite.spritecollide(self.lander, self.landing_sprites, False,
                                                          pygame.sprite.collide_mask)

        # If a collision was detected, check whether the lander has landed safely or crashed.
        if touched_landing_pad:
                if self.is_soft_landing(touched_landing_pad[0]):
                    self.lander.has_landed = True
                else:
                    self.lander.damage = 100
                    self.lander.has_crashed = True

    # Validates the landing as a soft landing otherwise indicates a crash.
    def is_soft_landing(self, landing_pad):
        if (0 < self.lander.velocity_y < 5 and -5 < self.lander.velocity_x < 5 and -3 < self.lander.angle < 3 and
                landing_pad.rect.collidepoint(self.lander.rect.bottomright) and
                landing_pad.rect.collidepoint(self.lander.rect.bottomleft)):
            return True
        else:
            return False

    # When this function is called it generates a group of meteors of varying numbers and sizes
    # at a random starting position out of the screen and adds them to the mission's hazards sprite group.
    def create_meteor_storm(self, settings):

        self.storm_is_active = True;

        # Picks a random number of meteors between 5 and 10
        meteor_count = random.randint(5, 10)

        # For the first meteor pick a random position among 400 pixels on the X axis,
        # either to the right or the left of the screen with a 50% chance.
        if random.randint(1, 100) >= 51:
            spawns_from = "Right"
            eye_of_storm_x = settings.screen_width + random.randint(-200, 200)
        else:
            spawns_from = "Left"
            eye_of_storm_x = random.randint(-200, 200)

        # On the Y axis the first meteor has a fixed starting position at -200 pixels.
        eye_of_storm_y = -200

        # Create the first meteor and add it to the hazards group.
        self.hazards.add(Meteor((eye_of_storm_x, eye_of_storm_y), spawns_from))

        for x in range(meteor_count - 1):

            # Create the next meteor at a starting position which deviates by 150 pixels to either side of each axis
            # with respect to the first meteor.
            new_meteor = Meteor((eye_of_storm_x + random.randint(-150, 150), eye_of_storm_y +
                                 random.randint(-150, 150)), spawns_from)

            # Keep repositioning the meteor as long as it overlaps another one.
            while True:
                overlapping_meteor = pygame.sprite.spritecollide(new_meteor, self.hazards, False,
                                                                 pygame.sprite.collide_mask)
                if overlapping_meteor:
                    new_meteor.rect.center = (eye_of_storm_x + random.randint(-150, 150), eye_of_storm_y +
                                              random.randint(-150, 150))
                else:
                    break

            # Add the new meteor in the group.
            self.hazards.add(new_meteor)

    # This function is called during each mission's set up phase and is responsible for creating
    # and initialising the static obstacles of the environment.
    def create_obstacles(self, settings):

        # Create a satellite at a random position in the upper-left portion of the screen
        # and keep repositioning it as long as it is overlapping any of the landing pads.
        while True:
            new_obstacle = Obstacle((random.randint(math.floor(50 * settings.screen_width / 1200), math.floor(480 *
                                                    settings.screen_width / 1200)),
                                     random.randint(math.floor(170 * settings.screen_height / 750), math.floor(325 *
                                                    settings.screen_height / 750))), "satellite_SE")
            overlapping_obstacle = pygame.sprite.spritecollide(new_obstacle, self.landing_sprites, False,
                                                               pygame.sprite.collide_mask)
            if overlapping_obstacle:
                new_obstacle.rect.center = (random.randint(math.floor(50 * settings.screen_width / 1200),
                                                           math.floor(480 * settings.screen_width / 1200)),
                                            random.randint(math.floor(170 * settings.screen_height / 750),
                                                           math.floor(325 * settings.screen_height / 750)))
            else:
                break

        # Add the satellite to the hazards sprite group.
        self.hazards.add(new_obstacle)

        # Create another satellite at a random position in the upper-right portion of the screen
        # and keep repositioning it as long as it is overlapping any of the landing pads.
        while True:
            new_obstacle = Obstacle((random.randint(math.floor(635 * settings.screen_width / 1200), math.floor(1130 *
                                                    settings.screen_width / 1200)),
                                     random.randint(math.floor(70 * settings.screen_height / 750), math.floor(400 *
                                                    settings.screen_height / 750))), "satellite_SW")
            overlapping_obstacle = pygame.sprite.spritecollide(new_obstacle, self.landing_sprites, False,
                                                               pygame.sprite.collide_mask)
            if overlapping_obstacle:
                new_obstacle.rect.center = (random.randint(math.floor(635 * settings.screen_width / 1200),
                                                           math.floor(1130 * settings.screen_width / 1200)),
                                            random.randint(math.floor(70 * settings.screen_height / 750),
                                                                    math.floor(400 * settings.screen_height / 750)))
            else:
                break

        # Add the satellite to the hazards sprite group.
        self.hazards.add(new_obstacle)

        # Create a building dome at a randomly selected starting position out of the three possible choices
        # and keep repositioning it as long as it is overlapping any of the landing pads.
        spawn_points = [(85 * settings.screen_width / 1200, 586 * settings.screen_height / 750),
                        (226 * settings.screen_width / 1200, 436 * settings.screen_height / 750),
                        (452 * settings.screen_width / 1200, 587 * settings.screen_height / 750)]
        while True:
            new_obstacle = Obstacle(spawn_points[random.randint(0, 2)], "building_dome")
            overlapping_obstacle = pygame.sprite.spritecollide(new_obstacle, self.landing_sprites, False,
                                                               pygame.sprite.collide_mask)
            if overlapping_obstacle:
                new_obstacle.rect.center = (spawn_points[random.randint(0, 2)])
            else:
                break

        # Add the building dome to the hazards sprite group.
        self.hazards.add(new_obstacle)

        # Create some rocks at a randomly selected starting position out of the two possible choices.
        spawn_points = [(560 * settings.screen_width / 1200, 570 * settings.screen_height / 750),
                        (695 * settings.screen_width / 1200, 595 * settings.screen_height / 750)]
        new_obstacle = Obstacle(spawn_points[random.randint(0, 1)], "rocks_ore_SW")

        # Add the rocks to the hazards sprite group.
        self.hazards.add(new_obstacle)

        # Create a pipe at a randomly selected starting position out of the two possible choices.
        spawn_points = [(1075 * settings.screen_width / 1200, 590 * settings.screen_height / 750),
                        (1130 * settings.screen_width / 1200, 520 * settings.screen_height / 750)]
        new_obstacle = Obstacle(spawn_points[random.randint(0, 1)], "pipe_stand_SE")

        # Add the pipe to the hazards sprite group.
        self.hazards.add(new_obstacle)

    # This function checks for collisions between the lander and any obstacles.
    def check_hits(self):

        # Check if the lander's frame overlaps any obstacle's frame.
        hazard_hit = pygame.sprite.spritecollide(self.lander, self.hazards, False,
                                                 pygame.sprite.collide_mask)
        for x in range(len(hazard_hit)):
            if not hazard_hit[x].is_touching:
                # Only damage the lander if this is the first frame at which the lander and the meteor-obstacle overlap.
                hazard_hit[x].is_touching = True
                self.lander.damage += hazard_hit[x].damage_caused
                # Damage cannot exceed 100%.
                if self.lander.damage >= 100:
                    self.lander.damage = 100

        # Clear the "first impact" flag for all meteors/obstacles that are no longer overlapping the lander.
        for x in self.hazards:
            if x.is_touching:
                if not pygame.sprite.collide_mask(self.lander, x):
                    x.is_touching = False
