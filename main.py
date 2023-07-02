"""
TSG4
"""
import random
from typing import List, Tuple

import pygame as pg

TITLE = "TSG4"
UPDATE_PERIOD = 1  # number of seconds between updates
resolution = (800, 800)
world_size = (4, 4)  # rows, cols)

counters = {"T": 1, "S": 1, "G": 1}


def evaluate_dims():
    cell_width = resolution[0] / world_size[0]
    cell_height = resolution[1] / world_size[1]

    return (cell_width, cell_height)


class BaseTSG:
    def __init__(self, prefix: str):
        self.energy = 1
        self.name = f"{prefix}{counters[prefix]}"
        counters[prefix] += 1


class Stuff(BaseTSG):
    def __init__(self, surface, row: int, col: int, size: int):
        super().__init__("S")
        self.surface = surface
        self.color = pg.Color(0, 10, 0)
        self.size = size / 2
        self.pos = (
            (size * ((row * size) // size)) + self.size,
            (size * ((col * size) // size)) + self.size,
        )

    def __str__(self):
        return f"{self.name}, pos: {self.pos}, size: {self.size}, energy: {self.energy}"

    def process(self, grow: bool):
        if grow:
            self.energy += 1
            self.color.g = min(200, 10 * self.energy)
            # print(str(self))

        # spawn a new stuff
        if self.energy > 200:
            print("spawn")

        self.draw()

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.pos, self.size)


class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()  # set to amx FPS
        pg.display.set_caption(TITLE)
        self.surface = pg.display.set_mode(resolution)
        self.loop = True
        self.cell_dims = evaluate_dims()
        self.last_update = 0
        self.stuffs_matrix: List[List[Stuff]] = [
            [None for col in range(world_size[0])] for row in range(world_size[1])
        ]

    def place_stuff(self):
        for row in range(world_size[0]):
            for col in range(world_size[1]):
                can_place = random.randint(0, 3)
                if can_place == 3:
                    self.stuffs_matrix[row][col] = Stuff(self.surface, row, col, self.cell_dims[0])
                    print(str(self.stuffs_matrix[row][col]))
                else:
                    self.stuffs_matrix[row][col] = None

    def process_stuff(self, grow: bool = False):
        for row in range(world_size[0]):
            for col in range(world_size[1]):
                stuff = self.stuffs_matrix[row][col]
                if stuff:
                    stuff.process(grow)

    def main(self):
        self.place_stuff()
        while self.loop:
            self.main_loop()

        pg.quit()

    def main_loop(self):
        self.clock.tick(30)
        self.surface.fill((0, 0, 0))
        # has enough time passed to perform an action?
        do_actions = False
        now = pg.time.get_ticks() / 1000
        if now - self.last_update > UPDATE_PERIOD:
            do_actions = True
            self.last_update = now

        # render alternating grid
        for row in range(world_size[0]):
            for col in range(row % 2, world_size[1], 2):
                rect = (
                    row * self.cell_dims[0],
                    col * self.cell_dims[1],
                    self.cell_dims[0],
                    self.cell_dims[1],
                )
                pg.draw.rect(self.surface, (40, 40, 40), rect)

        self.process_stuff(do_actions)

        # handle events
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    self.loop = False
                case pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.loop = False
                case pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    print(pos)
        pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.main()
