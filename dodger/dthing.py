import pygame as pg
import random


class Thing(pg.sprite.Sprite):

    def __init__(self, name, x_pos=0, y_pos=0):
        super().__init__()
        self.image = pg.image.load(name)
        self.x, self.y = x_pos, y_pos
        self.bild = self.image
        self.width = self.bild.get_width()
        self.height = self.bild.get_height()
        self.rect = self.bild.get_rect()

    def set_position(self, x_pos, y_pos, updown):
        self.x = x_pos
        if updown:
            y0_yu = random.randint(0, 1)
            self.y = y0_yu * y_pos + self.height / 2
        else:
            self.y = y_pos

    def move(self, xx, yy):
        self.x += xx
        self.y += yy

    def control_restart(self, xx, yy):
        if self.x < 0:
            y0_yu = random.randint(0, 1)
            self.x = xx - self.width / 2
            self.y = y0_yu * yy + self.height / 2
            return True
        else:
            return False
