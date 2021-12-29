import pygame
import random
import math

pygame.init()


class DrawInformation:
    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    BG_COLOUR = WHITE
    SIDE_PADDING = 100
    TOP_PADDING = 150
    FONT = pygame.font.SysFont('comicsans', 15)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    def __init__(self, width, height, arr):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Visualiser")

        self.set_array(arr)

    def set_array(self, arr):
        self.arr = arr
        self.min_value = min(arr)
        self.max_value = max(arr)

        self.block_width = round((self.width - self.SIDE_PADDING) / len(arr))
        self.block_height = math.floor((self.height - self.TOP_PADDING) / self.max_value)
        self.start_x = self.SIDE_PADDING // 2


def list_generator(n, min_value, max_value):
    arr = []
    for _ in range(n):
        value = random.randint(min_value, max_value)
        arr.append(value)
    return arr


def draw(draw_info, sorting_algo_name):
    draw_info.window.fill(draw_info.BG_COLOUR)
    title = draw_info.LARGE_FONT.render(sorting_algo_name, 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))
    controls = draw_info.FONT.render("R => RESET | SPACE => START SORTING", 1, draw_info.BLACK)
    draw_info.window.blit(controls, ((draw_info.width / 2) - (controls.get_width() / 2), 45))
    sort = draw_info.FONT.render("I => INSERTION SORT | B => BUBBLE SORT", 1,
                                 draw_info.BLACK)
    draw_info.window.blit(sort, ((draw_info.width / 2) - (sort.get_width() / 2), 60))
    draw_array(draw_info)
    pygame.display.update()


def draw_array(draw_info, colour_positions={}, clear_bg=False):
    arr = draw_info.arr
    if clear_bg:
        clear_rect = ((draw_info.SIDE_PADDING // 2), draw_info.TOP_PADDING, (draw_info.width - draw_info.SIDE_PADDING),
                      draw_info.height)
        pygame.draw.rect(draw_info.window, draw_info.BG_COLOUR, clear_rect)
    for i, value in enumerate(arr):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (draw_info.block_height * value)
        colour = draw_info.GREY
        if i in colour_positions:
            colour = colour_positions[i]
        pygame.draw.rect(draw_info.window, colour, (x, y, draw_info.block_width, draw_info.height))
        pygame.draw.rect(draw_info.window, draw_info.BLACK, (x, y, draw_info.block_width, draw_info.height), 1)
    if clear_bg:
        pygame.display.update()


def bubble_sort(draw_info):
    arr = draw_info.arr

    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            num1 = arr[j]
            num2 = arr[j + 1]

            if num1 > num2:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_array(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return arr

def insertion_sort(draw_info):
    arr = draw_info.arr
    for i in range(len(arr)):
        j=i
        while j>0 and arr[j-1]>arr[j]:
            arr[j-1],arr[j]=arr[j],arr[j-1]
            j-=1
            draw_array(draw_info, {j - 1: draw_info.GREEN, j: draw_info.RED}, True)
            yield True
    return arr

def main():
    run = True
    clock = pygame.time.Clock()
    n = 20
    min_value = 0
    max_value = 100
    arr = list_generator(n, min_value, max_value)
    draw_info = DrawInformation(800, 600, arr)
    sorting = False
    sorting_algorithm = bubble_sort
    sorter = None
    sorting_algo_name = "Bubble Sort"

    while run:
        clock.tick(5)

        if sorting:
            try:
                next(sorter)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info,sorting_algo_name)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    arr = list_generator(n, min_value, max_value)
                    draw_info.set_array(arr)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorter = sorting_algorithm(draw_info)
                    sorting = True
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "Bubble Sort"

                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "Insertion Sort"
    pygame.quit()


if __name__ == "__main__":
    main()
