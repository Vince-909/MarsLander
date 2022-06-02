

# This class implements the "breathing" visual effect used to highlight
# the currently selected option on the menu screen (slow mode)
# and also used with the * ALERT !!! * message of the instruments panel (fast mode).
class Breather:
    def __init__(self, mode):
        if mode == "slow":
            self.speed = 2
        elif mode == "fast":
            self.speed = 15
        self.color_value = 255
        self.color_value_increases = False

    def breathe(self):
        if self.color_value_increases:
            self.color_value += self.speed
            if self.color_value >= 255:
                self.color_value = 255
                self.color_value_increases = False
        else:
            self.color_value -= self.speed
            if self.color_value <= 50:
                self.color_value_increases = True


# This class handles the mixing of the red and green color values that make up the font color for the damage indicator,
# in such a way that the resulting color value will be more green for low damage levels and more towards the red side
# for damage levels close to 100%.
class RedGreenMixer:
    def __init__(self):
        self.green_fuel = 255
        self.red_fuel = 0
        self.green_damage = 255
        self.red_damage = 0

    def mix_fuel(self, fuel):
        if fuel <= 500:
            self.red_fuel = 255
            self.green_fuel = fuel * 255 / 500
        else:
            self.green_fuel = 255
            self.red_fuel = 255 - (fuel - 500) * 255 / 500

    def mix_damage(self, damage):
        if damage <= 50:
            self.green_damage = 255
            self.red_damage = damage * 255 / 50
        else:
            self.red_damage = 255
            self.green_damage = 255 - (damage - 50) * 255 / 50
