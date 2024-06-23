import pygame as pg


class Game:

    def __init__(self, color):
        self.start = 0
        self.score = 0
        self.text_ = pg.Surface((300, 50))  # create a text field
        self.text_.fill(color)

    # information output
    def show_message(self, text, color):
        self.font = pg.font.SysFont('arial', 48)
        self.text_ = self.font.render(text, True, color)

    # counting and outputting points
    def set_score(self, num, color):
        self.score += num
        self.show_message('Score: ' + str(self.score), color)

    # timer
    def get_time(self, reset):
        if reset:
            self.start = pg.time.get_ticks()
        self.diff = pg.time.get_ticks() - self.start
        return self.diff

    # score and time
    def show_all(self, num, color):
        self.score += num
        ptext = ' |  Score: ' + str(self.score)
        ztext = 'Time: ' + str(int(self.diff / 1000))
        self.show_message(ztext + ptext, color)
