# -*- coding: utf-8 -*-

"""Game: PaddleBall
[Python для детей. Джейсон Бриггс (2017)]

Разработайте игру с прыгающим мячом и ракеткой. Мяч будет летать по экрану,
а игрок - отбивать его ракеткой. Если мяч коснется нижней границы экрана,
игра завершится. Реализуйте начало игры по клику левой клавиши мыши, счетчик
количества отскоков от ракетки и сообщение об окончании игры.
"""

from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color):
        # canvas
        self.canvas = canvas
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # paddle
        self.paddle = paddle
        # ball
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        # msg 'Game over!'
        self.msg_id = canvas.create_text(250, 150,
                                         text='Game over!',
                                         fill='black',
                                         font=('Hevletica 20 bold'),
                                         state='hidden')
        # score
        self.score = 0
        self.score_id = canvas.create_text(470, 20,
                                           text = str(self.score),
                                           fill='black',
                                           font=('Hevletica 20 bold'))
        # other
        self.hit_bottom = True
        self.canvas.bind_all('<Button-1>', self.start)

    def start(self, event):
        # hide msg 'Game over!'
        self.canvas.itemconfig(self.msg_id, state='hidden')
        # reset score
        self.score = 0
        self.canvas.itemconfig(self.score_id, text=str(self.score))
        # set the ball in place
        self.canvas.coords(self.id, 10, 10, 25, 25)
        self.canvas.move(self.id, 245, 100)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        # update
        self.canvas.update()
        # pause
        time.sleep(0.5)
        # run
        self.hit_bottom = False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <=paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= self.canvas_height:
            # stop game
            self.hit_bottom = True
            # show msg 'Game over!'
            self.canvas.itemconfig(self.msg_id, state='normal')
        if self.hit_paddle(pos) == True:
            self.y = -3
            # increase score
            self.score += 1
            self.canvas.itemconfig(self.score_id, text=str(self.score))

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
            self.canvas.move(self.id, pos[0] * -1, 0)
        elif pos[2] >= self.canvas_width:
            self.x = 0
            self.canvas.move(self.id, (pos[2] - self.canvas_width) * -1, 0)
            
    def turn_left(self, evt):
        self.x = -4

    def turn_right(self, evt):
        self.x = 4

tk = Tk()
tk.title('Game - PaddleBall')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red')

while True:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
