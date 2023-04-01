# -*- coding: utf-8 -*-

"""Game: StickMan
[Python для детей. Джейсон Бриггс (2017)]
"""

from tkinter import *
import random
import time

class Game:
    def __init__(self):
        # create window
        self.tk = Tk()
        self.tk.title('Mr. Stick Man Races for the Exit')  # set title
        self.tk.resizable(0, 0)  # set no resizable
        self.tk.wm_attributes('-topmost', 1)  # set over all windows

        # create canvas
        self.canvas_width = 500
        self.canvas_height = 500
        self.canvas = Canvas(self.tk,
                             width=self.canvas_width,
                             height=self.canvas_height,
                             highlightthickness=0)  # remove border
        self.canvas.pack()
        self.tk.update()

        # draw background
        self.bg = PhotoImage(file='images/background.gif')  # img fragment
        # get fragment size
        w = self.bg.width()
        h = self.bg.height()
        # tile the screen with fragments
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x * w, y * h,
                                         image=self.bg,
                                         anchor='nw')
        self.sprites = []  # list all sprites
        self.running = True  # flag game is running

    def mainloop(self):
        while True:
            # if the game is running move all sprites
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
            # update window
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)

class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

# checking the intersection of objects by x
def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
        or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
        or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
        or (co2.x2 > co1.x1 and co2.x2 < co1.x2):
        return True
    else:
        return False

# checking the intersection of objects by y
def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
        or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
        or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
        or (co2.y2 > co1.y1 and co2.y2 < co1.y2):
        return True
    else:
        return False

# checking left side collision
def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <=co2.x2 and co1.x1 >= co2.x1:
            return True
    return False

# checking right side collision
def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False

# checking top collision
def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False

# checking bottom collision
def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height, mov):
        Sprite.__init__(self, game)
        # draw platform sprite
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y,
                                              image=self.photo_image,
                                              anchor='nw')
        # set sprite coordinates
        self.coordinates = Coords(x, y, x + width, y + height)
        # parametes for moving
        self.x = -1
        self.width = width
        self.mov = mov

    def move(self):
        if self.mov:  # if platform can move
            # get sprite coordinates
            co = self.coords()
            # if sprite moves left and x <= 0 - reverse
            if self.x < 0 and co.x1 <= 0:
                self.x *= -1
            # if sprite moves right and x > canvas width - reverse
            if self.x > 0 and co.x2 >= self.game.canvas_width:
                self.x *= -1
            # move sprite
            self.game.canvas.move(self.image, self.x, 0)
            # get new coordinates
            new_co = self.game.canvas.coords(self.image)
            # save new coordinates
            co.x1 = new_co[0]
            co.x2 = new_co[0] + self.width

class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        # list of all left position of stickfigure sprite
        self.images_left = [
            PhotoImage(file='images/figure-L1.gif'),
            PhotoImage(file='images/figure-L2.gif'),
            PhotoImage(file='images/figure-L3.gif')
        ]
        # list of all right position of stickfigure sprite
        self.images_right = [
            PhotoImage(file='images/figure-R1.gif'),
            PhotoImage(file='images/figure-R2.gif'),
            PhotoImage(file='images/figure-R3.gif')
        ]
        # draw start position of stickfigure
        self.image = game.canvas.create_image(200, 470,
                                              image=self.images_left[0],
                                              anchor='nw')
        # set initial settings
        self.x = -2  # speed x
        self.y = 0  # speed y
        self.current_image = 0  # initial sprite
        self.current_image_add = 1  # sprite switching step
        self.jump_count = 0
        self.last_time = time.time()  # time elapsed from switching sprite
        self.coordinates = Coords()  # initial coordinates
        # control
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:  # if not jumping
            self.x = -2

    def turn_right(self, evt):
        if self.y == 0:  # if not jumping
            self.x = 2

    def jump(self, evt):
        if self.y == 0:  # if not jumping
            self.y = -4  # set speed y
            self.jump_count = 0  # reset jump count

    def animate(self):
        # if stickfigure run and not jumping
        if self.x != 0 and self.y == 0:
            # if more than 0.1 second has passed since changing the picture
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()  # set new last time
                self.current_image += self.current_image_add  # set next picture
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        # if stickfigure runs left and jumping
        if self.x < 0:
            if self.y != 0:
                # change picture for jumping
                self.game.canvas.itemconfig(self.image, \
                            image=self.images_left[2])
            # else change picture for runing
            else:
                self.game.canvas.itemconfig(self.image, \
                            image=self.images_left[self.current_image])
        # if stickfigure runs right and jumping
        elif self.x > 0:
            if self.y != 0:
                # change picture for jumping
                self.game.canvas.itemconfig(self.image, \
                            image=self.images_right[2])
            # else change picture for runing
            else:
                self.game.canvas.itemconfig(self.image, \
                            image=self.images_right[self.current_image])

    def coords(self):
        # get stickfigure coordinates
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        # animate
        self.animate()
        # if stickfigure is jumping up
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        # if stickfigure is jumping down
        if self.y > 0:
            self.jump_count -= 1
        # get coordinates
        co = self.coords()
        # side stickfigure for checking
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        # CHECKING TOUCH TO THE WINDOW
        # if stickfigure jumping down and touch down
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0  # set speed y = 0
            bottom = False  # no need to check bottom
        # if stickfigure jumping up and touch top of window
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0  # set speed y = 0
            top = False  # no need to check top
        # if stickfigure runs right and touch right side of window
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0  # set speed x = 0
            right = False  # no need to check right
        # if stickfigure runs and touch left side of window
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0  # set speed x = 0
            left = False  # no need to check left

        # CHECKING TOUCH TO SPRITES
        # checking for collisions with all sprites
        for sprite in self.game.sprites:
            # don't check yourself
            if sprite == self:
                continue
            # get sprite's coordinates
            sprite_co = sprite.coords()
            # if stickfigure jumping up, don't touch top and collided top
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y  # change direction of speed y
                top = False  # no need to check top
            # if stickfigure jumping down, don't touch down and collided bottom
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0  # set speed y = 0
                bottom = False  # no need to check bottom
                top = False  # no need to check top
            # if the sprite fell
            if bottom and falling and self.y == 0 \
                    and co.y2 < self.game.canvas_height \
                    and collided_bottom(1, co, sprite_co):
                falling = False  # no need to check falling
            # if stickfigure runs left and collided left
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0  # set speed x = 0
                left = False  # no need to check left
                if sprite.endgame:
                    door.open_door()
            # if stickfigure runs right and collided right
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0  # set speed x = 0
                right = False  # no need to check right
                if sprite.endgame:
                    door.open_door()
        # if stickfigure keeps falling
        if falling and bottom and self.y == 0 \
                and co.y2 < self.game.canvas_height:
            self.y = 4  # set speed y = 4
        # move stickfigure according to new parameters
        self.game.canvas.move(self.image, self.x, self.y)

    def hide(self):
        self.game.canvas.itemconfig(self.image, state='hidden')

class DoorSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        # door size
        self.x = 45
        self.y = 30
        self.width = 40
        self.height = 35
        # pictures of doors
        self.images = [PhotoImage(file='images/door1.gif'),
                       PhotoImage(file='images/door2.gif')]
        # draw door
        self.image = game.canvas.create_image(self.x, self.y, \
                                              image=self.images[0],
                                              anchor='nw')
        self.coordinates = Coords(self.x, self.y, self.x + (self.width / 2),
                                  self.y + self.height)
        self.endgame = True

    def open_door(self):
        self.game.tk.update()
        # open the door
        self.game.canvas.itemconfig(self.image, image=self.images[1])
        self.game.tk.update()
        time.sleep(0.5)
        # hide stickfigure
        sf.hide()
        self.game.tk.update()
        time.sleep(0.5)
        # close the door
        self.game.canvas.itemconfig(self.image, image=self.images[0])
        self.game.tk.update()
        time.sleep(0.5)
        # show message "You win!"
        self.game.canvas.itemconfig(msg_id, state='normal')
        # stop game
        self.game.running = False

# create instance game
g = Game()
# create platforms
platforms = {  # dict consists all data of platforms
    'platform1.gif' : [(0, 480, 100, 10, True),
                       (150, 440, 100, 10, True),
                       (300, 400, 100, 10, True),
                       (300, 160, 100, 10, True)],
    'platform2.gif' : [(175, 350, 66, 10, True),
                       (50, 300, 66, 10, True),
                       (170, 120, 66, 10, True),
                       (45, 60, 66, 10, False)],
    'platform3.gif' : [(170, 250, 32, 10, True),
                       (230, 200, 32, 10, True)]
}
for platform_name, platform_coords in platforms.items():
    for x, y, width, height, mov in platform_coords:
        platform = PlatformSprite(g, PhotoImage(file=f'images/{platform_name}'),
                                  x, y, width, height, mov)
        g.sprites.append(platform)
# create door
door = DoorSprite(g)
g.sprites.append(door)
# create stickfigure
sf = StickFigureSprite(g)
g.sprites.append(sf)
# create message "You win!"
msg_id = g.canvas.create_text(250, 220, text='You win!', fill='white', \
                   font=('Hevletica 30 bold'), state='hidden')
g.mainloop()
