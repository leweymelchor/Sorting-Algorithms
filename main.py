import pygame as pg
import random

pg.init ()

class DrawInformation:
    BLACK = 0, 0,
    WHITE = 255, 255,255
    GREEN = 0, 255, 0
    RED = 255,0, 0
    GREY = 128, 128, 128
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [
        GREY,
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pg.display.set_mode((width, height))
        pg.display.set_caption('Sorting Visualizer')

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)

        self.bar_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.bar_height = round((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)
    pg.display.update()

def draw_list(draw_info):
    lst = draw_info.lst

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.bar_height

        color = draw_info.GRADIENTS[i % 3]

        pg.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height ))

def generate_starting_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def main():
    run = True
    clock = pg.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    while run:
        clock.tick(60)
        draw(draw_info)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
    pg.quit()


if __name__ == "__main__":
    main()
