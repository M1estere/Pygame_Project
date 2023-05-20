import pygame

from misc.settings import *

from random import randint, uniform

class Raindrop:
    def __init__(self, window):
        self.x = randint(5, WIDTH)
        self.y = randint(-HEIGTH, 0)

        self.z = randint(0, 30)
        self.width = randint(0, 2)
        self.colour = TEXT_COLOUR
        self.window = window

        self.y_speed = 5

    def fall(self):
        self.y += self.y_speed
        self.y_speed += (0.025 * self.z) / 30

        if self.y >= 700:
            self.y = randint(-200, -100)
            self.y_speed = uniform(2.5, 2)

    def display(self):
        pygame.draw.rect(self.window, self.colour, (self.x, self.y, self.width, 7))