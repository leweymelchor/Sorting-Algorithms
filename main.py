import pygame as pg
import random
import math

pg.init ()

class DrawInformation:
    BLACK = 0, 0, 0
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
    FONT = pg.font.SysFont('futura', 20)
    LARGE_FONT = pg.font.SysFont('futura', 35)

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
        self.bar_height = math.floor((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)
    draw_list(draw_info)

    controls = draw_info.FONT.render(
        "Reset: Space Bar | Sort: Return | Ascending: a | Descending: d", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/ 2 - controls.get_width() / 2, 5))

    sorting = draw_info.FONT.render(
        "Insertion Sort: i | Bubble Sort: b", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/ 2 - sorting.get_width() / 2, 25))

    draw_list(draw_info)
    pg.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
                       draw_info.width - draw_info.SIDE_PAD,
                         draw_info.height - draw_info.TOP_PAD)
        pg.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.bar_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pg.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height ))

    if clear_bg:
        pg.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True
    return lst

def main():
    run = True
    clock = pg.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_name = "Bubble Sort"
    sorting_alg_generator = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_alg_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info)

        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type != pg.KEYDOWN:
                continue
            if event.key == pg.K_SPACE:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting == False
            elif event.key == pg.K_RETURN and sorting == False:
                sorting = True
                sorting_alg_generator = sorting_alg(draw_info, ascending)
            elif event.key == pg.K_a and not sorting:
                ascending = True
            elif event.key == pg.K_d and not sorting:
                ascending = False



    pg.quit()


if __name__ == "__main__":
    main()
