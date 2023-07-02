"""
TSG4
"""
import random
from typing import List, Optional, Tuple

import pygame as pg

TITLE = "TSG4"
UPDATE_PERIOD = 0.01  # number of seconds between updates
TICK_SPEED = 1000
resolution = (800, 800)
WORLD_WIDTH = 40
WORLD_HEIGHT = 40
STUFF_CHANCE = 10

counters = {"T": 1, "S": 1, "G": 1}


def evaluate_dims() -> Tuple[float, float]:
    """
    Get base cell width and height base on resolution and world dimensions
    """
    cell_width = resolution[0] / WORLD_WIDTH
    cell_height = resolution[1] / WORLD_HEIGHT

    return (cell_width, cell_height)


class BaseTSG:
    """
    Base class for TSG classes.
    """

    def __init__(self, surface: pg.Surface, prefix: str, row: int, col: int, color: pg.Color):
        self.surface = surface
        self.energy = 1
        self.age = 0
        self.lifespan = 0
        self.spawn_threshold = 0
        self.row = row
        self.col = col
        self.color = color
        self.dead = False  # is this instnace alive or dead
        self.name = f"{prefix}{counters[prefix]}"
        counters[prefix] += 1

    def draw(self):
        pass

    def process(self, do_actions: bool):
        pass


class Stuff(BaseTSG):
    """
    Stuff - this grows on the substrate of the World.
    It gains energy at a set rate, and will spawn new stuff in empty spaces next to it
    """

    def __init__(self, manager, surface, row: int, col: int, size: int):
        super().__init__(surface, "S", row, col, pg.Color(0, 10, 0))
        self.manager = manager
        self.size = size / 2
        self.lifespan = 50
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.pos = (
            (size * ((row * size) // size)) + self.size,
            (size * ((col * size) // size)) + self.size,
        )

    def __str__(self):
        return f"{self.name}, cell: ({self.row},{self.col}), age: {self.age}, energy: {self.energy}"

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.eat()
            self.spawn()
            self.die()

        self.draw()

    def eat(self):
        self.energy += 1
        self.age += 1
        self.color.g = min(200, 10 * self.energy)

    def spawn(self):
        # spawn a new stuff
        if self.energy > self.spawn_threshold:
            # check for free adjacent squares in manager
            has_free_cell, row, col = self.manager.get_next_free_cell(self.row, self.col)

            if has_free_cell:
                self.manager.add_stuff(row, col)
                self.energy = int(self.energy / 2)
            else:
                self.die(True)

    def die(self, force: bool = False):
        if force or self.age > self.lifespan:
            self.dead = True

        if self.dead:
            self.color = pg.Color(255, 0, 0)

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.pos, self.size)


class BaseManager:
    """
    Base Maanger for TSG instances
    """

    def __init__(self, surface: pg.Surface, cell_dims: Tuple[int, int]):
        self.surface = surface
        self.cell_dims = cell_dims
        self.matrix: List[List[Optional[BaseTSG]]] = [
            [None for col in range(WORLD_WIDTH)] for row in range(WORLD_HEIGHT)
        ]

    def get_next_free_cell(self, row, col) -> Tuple[bool, int, int]:
        """
        Find the next empty cell in the matrix starting top left and moving clockwise
        """
        # check adjacent cells to passed row and col
        if (row - 1 >= 0) and (col - 1 >= 0) and self.matrix[row - 1][col - 1] is None:
            return (True, row - 1, col - 1)
        if (row - 1 >= 0) and self.matrix[row - 1][col] is None:
            return (True, row - 1, col)
        if (row - 1 >= 0) and (col + 1 < WORLD_HEIGHT) and self.matrix[row - 1][col + 1] is None:
            return (True, row - 1, col + 1)

        if (col - 1 >= 0) and self.matrix[row][col - 1] is None:
            return (True, row, col - 1)
        if (col + 1 < WORLD_HEIGHT) and self.matrix[row][col + 1] is None:
            return (True, row, col + 1)

        if (row + 1 < WORLD_WIDTH) and (col - 1 >= 0) and self.matrix[row + 1][col - 1] is None:
            return (True, row + 1, col - 1)
        if (row + 1 < WORLD_WIDTH) and self.matrix[row + 1][col] is None:
            return (True, row + 1, col)
        if (
            (row + 1 < WORLD_WIDTH)
            and (col + 1 < WORLD_HEIGHT)
            and self.matrix[row + 1][col + 1] is None
        ):
            return (True, row + 1, col + 1)

        return (False, row, col)

    def remove(self, row: int, col: int):
        """
        Remove TSG instance from matrix
        """
        self.matrix[row][col] = None


class StuffManager(BaseManager):
    """
    Manages the Stuff instances in the World.

    - randomly places stuff at creation
    - culls dead stuff
    - pokes stuff to process their actions
    """

    def __init__(self, surface: pg.Surface, cell_dims: Tuple[int, int]):
        super().__init__(surface, cell_dims)
        self.place_chance = STUFF_CHANCE

    def place_stuff(self):
        """
        Initial World with randomly placed Stuff
        """
        for row in range(WORLD_WIDTH):
            for col in range(WORLD_HEIGHT):
                can_place = random.randint(0, STUFF_CHANCE)
                if can_place == self.place_chance:
                    self.add_stuff(row, col)

    def add_stuff(self, row: int, col: int):
        """
        Add a new Stuff instance to the matrix
        :param row: which row
        :param col: which col
        """
        self.matrix[row][col] = Stuff(self, self.surface, row, col, self.cell_dims[0])

    def cull_stuff(self):
        """
        Cull Stuff marked as 'dead' from the matrix
        """
        for row in range(WORLD_WIDTH):
            for col in range(WORLD_HEIGHT):
                stuff = self.matrix[row][col]
                if stuff and stuff.dead:
                    self.remove(row, col)

    def process_stuff(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Stuff is present,
        tell it to process its actions
        """
        for row in range(WORLD_WIDTH):
            for col in range(WORLD_HEIGHT):
                stuff = self.matrix[row][col]
                if stuff:
                    stuff.process(do_actions)


class Game:
    """
    Manages the game
    - draws the substrate
    - handles TSG managers
    """

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()  # set to amx FPS
        pg.display.set_caption(TITLE)
        self.surface = pg.display.set_mode(resolution)
        self.loop = True
        self.cell_dims = evaluate_dims()
        self.last_update = 0
        self.num_ticks = 0
        self.font = pg.font.SysFont("Arial", 20)
        self.stuff_manager = StuffManager(self.surface, self.cell_dims)

    def main(self):
        """
        Main entry point and set up
        """

        self.stuff_manager.place_stuff()
        while self.loop:
            self.main_loop()

        pg.quit()

    def main_loop(self):
        """
        Main loop
        - checks clock for next action tick
        - renders substrate
        - calls manager methods
        - displays number of action ticks so far
        - event handling
        """
        self.clock.tick(30)
        self.surface.fill((0, 0, 0))
        # has enough time passed to perform an action?
        do_actions = False
        now = pg.time.get_ticks() / TICK_SPEED
        if now - self.last_update > UPDATE_PERIOD:
            do_actions = True
            self.last_update = now
            self.num_ticks += 1

        # render alternating grid
        for row in range(WORLD_WIDTH):
            for col in range(row % 2, WORLD_HEIGHT, 2):
                rect = (
                    row * self.cell_dims[0],
                    col * self.cell_dims[1],
                    self.cell_dims[0],
                    self.cell_dims[1],
                )
                pg.draw.rect(self.surface, (40, 40, 40), rect)

        self.stuff_manager.cull_stuff()
        self.stuff_manager.process_stuff(do_actions)

        tick_text = f"Tick: {self.num_ticks}"
        ren = self.font.render(tick_text, 0, (250, 240, 230), (5, 5, 5))
        self.surface.blit(ren, (10, 10))

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
