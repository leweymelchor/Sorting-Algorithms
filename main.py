import pygame as pg
import random
import math

pg.init ()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255,255
    GREEN = 145, 127, 179
    RED = 42, 47, 79
    GREY = 128, 128, 128
    BACKGROUND_COLOR = 231, 203, 203

    GRADIENTS = [
        (255, 187, 92),
        (255, 155, 80),
        (226, 94, 62)
    ]
    FONT = pg.font.SysFont('futura', 20)
    LARGE_FONT = pg.font.SysFont('futura', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    TOP = pg.Color(99, 89, 133)
    BOTTOM = pg.Color(145, 127, 179)
    BAND_HEIGHT = 1


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


def draw(draw_info, alg_name, ascending):
    draw_grad(draw_info)
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    draw_list(draw_info)

    title = draw_info.LARGE_FONT.render(
        f"{alg_name}: {'Ascending' if ascending else 'Descending'}", 1, draw_info.RED)
    draw_info.window.blit(title, (draw_info.width/ 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render(
        "Reset: Space Bar | Sort: Return | Ascending: a | Descending: d", 1, draw_info.RED)
    draw_info.window.blit(controls, (draw_info.width/ 2 - controls.get_width() / 2, 45))

    sorting = draw_info.FONT.render(
        "Bubble Sort: b | Insertion Sort: i | Selection Sort | s", 1, draw_info.RED)
    draw_info.window.blit(sorting, (draw_info.width/ 2 - sorting.get_width() / 2, 70))

    speed = draw_info.FONT.render(
        "Speed: 1, 2, 3, 4", 1, draw_info.RED)
    draw_info.window.blit(speed, (25, 45))

    draw_list(draw_info)
    pg.display.update()


def draw_grad(draw_info):

    for y in range(0, draw_info.height, draw_info.BAND_HEIGHT):
        lerped_color = (
        int(draw_info.TOP[0] + (draw_info.BOTTOM[0] - draw_info.TOP[0]) * y / (draw_info.height)),
        int(draw_info.TOP[1] + (draw_info.BOTTOM[1] - draw_info.TOP[1]) * y / (draw_info.height)),
        int(draw_info.TOP[2] + (draw_info.BOTTOM[2] - draw_info.TOP[2]) * y / (draw_info.height)))

        pg.draw.rect(draw_info.window, lerped_color, (0, y, draw_info.width, draw_info.BAND_HEIGHT))


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

        pg.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height), 0, 9, 9)

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


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and  not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current

            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)):

        # Find the minimum element in remaining
        # unsorted array
        min_idx = i

        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j] and ascending or lst[min_idx] < lst[j] and not ascending:
                min_idx = j

        # Swap the found minimum element with
        # the first element
        lst[i], lst[min_idx] = lst[min_idx], lst[i]

        draw_list(draw_info, {i: draw_info.GREEN, min_idx: draw_info.RED}, True)
        yield True

    return lst


def main():
    run = True
    clock = pg.time.Clock()
    speed = 30

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(1200, 600, lst)
    sorting = False
    ascending = True

    sorting_alg = bubble_sort
    sorting_alg_name = "Bubble Sort"
    sorting_alg_generator = None

    while run:
        clock.tick(speed)

        if sorting:
            try:
                next(sorting_alg_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_alg_name, ascending)

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

            elif event.key == pg.K_i and not sorting:
                sorting_alg = insertion_sort
                sorting_alg_name = "Insertion Sort"
            elif event.key == pg.K_b and not sorting:
                sorting_alg = bubble_sort
                sorting_alg_name = "Bubble Sort"
            elif event.key == pg.K_s and not sorting:
                sorting_alg = selection_sort
                sorting_alg_name = "Selection Sort"

            elif event.key == pg.K_1:
                speed = 3.5
            elif event.key == pg.K_2:
                speed = 7
            elif event.key == pg.K_3:
                speed = 15
            elif event.key == pg.K_4:
                speed = 120




    pg.quit()


if __name__ == "__main__":
    main()
