import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, x_pos=0, y_pos=0):
        super().__init__()
        self.image = pg.image.load("insect1.png")
        self.x, self.y = x_pos, y_pos
        self.bild = self.image
        self.is_killed = False

    def rotate(self, degree):
        self.bild = pg.transform.rotate(self.image, degree)

    def move(self, distance, xx, yy):
        self.x += xx
        self.y += yy
        distance -= 1
        return distance

    def step(self, xx, yy):
        self.x += xx
        self.y += yy

    def destroy(self):
        self.image = pg.image.load("insect2x.png")
        self.bild = self.image
        self.is_killed = True
