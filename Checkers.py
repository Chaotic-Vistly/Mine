from turtle import *

SCALE_X = 80
SCALE_Y = 80
OFFSET_X = -4
OFFSET_Y = 3

class Square:
    def __init__(self, points, sx = SCALE_X, sy = SCALE_Y, ox = OFFSET_X, oy = OFFSET_Y, lc = 'black', fc = 'black'):
        self.list_points = points
        self.scale_x = sx
        self.scale_y = sy
        self.offset_x = ox
        self.offset_y = oy
        self.line_color = lc
        self.fill_color = fc

    def scale_it(self, point):
        goto((point['x'] + self.offset_x) * self.scale_x, (point['y'] + self.offset_y) * self.scale_y)

    def draw_it(self):
        pencolor(self.line_color)
        fillcolor(self.fill_color)
        penup()
        self.scale_it(self.list_points[0])
        pendown()
        begin_fill()
        for i in self.list_points:
            self.scale_it(i)
        end_fill()

square = [
    {'x': 0, 'y': 0}, {'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'x': 0, 'y': 1}, {'x': 0, 'y': 0}
]

def draw_check():
    speed(0)
    hideturtle()

    for row in range(8):
        for col in range (8):
            color = "black" if (row + col) % 2 == 0 else 'white'
            offset_x = col
            offset_y = -row
            Checker = Square(
                square,
                sx= SCALE_X,
                sy= SCALE_Y,
                ox = offset_x + OFFSET_X,
                oy = offset_y + OFFSET_Y,
                fc = color
            )
            Checker.draw_it()

draw_check()
done()