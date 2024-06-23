from math import *
import random
from bplayer import *
from game import *

# setting initial values
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
x_max, y_max = 600, 400
direction = 0
distance = 0
degree = 0
bug_max = 5

# launching Pygame, creating a game field and character
pg.init()
pg.key.set_repeat(20, 20)
pg.display.set_caption("Bug Game")
window = pg.display.set_mode((x_max, y_max))
arcade = Game(green)

figure = []
for nr in range(0, bug_max):
    x_pos = random.randint(100, x_max - 100)
    y_pos = random.randint(50, y_max - 100)
    figure.append(Player(x_pos, y_pos))


# random direction
x_step = []
y_step = []

for nr in range(0, bug_max):
    x_step.append(random.randint(0, 2))
    if x_step[nr] == 0:
        x_step[nr] = -1
    y_step.append(random.randint(0, 2))
    if y_step[nr] == 0:
        y_step[nr] = -1

# start timer
arcade.get_time(True)

# event loop
running = True
while running:
    # check and output time
    time = arcade.get_time(False)
    arcade.show_all(0, blue)

    # when time is gone
    if time > bug_max * 1500:
        arcade.show_message('Game Over', red)
        running = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        # setting the mouse
        if event.type == pg.MOUSEBUTTONDOWN:
            (x_pos, y_pos) = pg.mouse.get_pos()

            for nr in range(0, bug_max):
                if (figure[nr].x < x_pos < figure[nr].x + 100
                        and figure[nr].y < y_pos < figure[nr].y + 100):
                    if not figure[nr].is_killed:
                        arcade.set_score(50, blue)
                    figure[nr].destroy()

    # restriction of movement
    for nr in range(0, bug_max):
        if figure[nr].x < 0 or figure[nr].x > x_max - 110:
            x_step[nr] = -x_step[nr]
        if figure[nr].y < 0 or figure[nr].y > y_max - 110:
            y_step[nr] = -y_step[nr]

    # determining the direction of movement
    for nr in range(0, bug_max):
        degree = atan2(-y_step[nr], x_step[nr])
        degree = degrees(degree) - 90
        figure[nr].rotate(degree)

    # motion delay
    for nr in range(0, bug_max):
        if not figure[nr].is_killed:
            figure[nr].step(x_step[nr] * 2, y_step[nr] * 2)
            pg.time.delay(5)

    # sprite position in window (new)
    window.fill(green)
    window.blit(arcade.text_, (x_max / 3, 10))
    for nr in range(0, bug_max):
        window.blit(figure[nr].bild, (figure[nr].x, figure[nr].y))
    pg.display.update()

pg.time.delay(1500)
pg.quit()
