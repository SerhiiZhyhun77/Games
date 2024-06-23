import pygame as pg


class Player(pg.sprite.Sprite):
    image = []

    def __init__(self, x_pos=0, y_pos=0):
        super().__init__()
        self.image.append(pg.image.load("images/do_stand.png"))
        self.image.append(pg.image.load("images/do_duck.png"))
        self.image.append(pg.image.load("images/do_jump.png"))
        self.x, self.y = x_pos, y_pos
        self.bild = self.image[0]
        self.is_hit = False
        self.status = 0

    def set_state(self, nr):
        self.status = nr
        self.bild = self.image[nr]

    def dodge(self, y_pos, y_middle):
        if ((y_pos < y_middle and self.status == 1)
                or (y_pos > y_middle and self.status == 2)):
            return True
        else:
            return False
