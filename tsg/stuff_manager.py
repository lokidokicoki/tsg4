"""
Manages the Stuff instances in the World.
"""
import random
from typing import Tuple

import pygame as pg

from tsg import BaseManager, Cell, Stuff, TSGConfig


class StuffManager(BaseManager):
    """
    Manages the Stuff instances in the World.

    - randomly places stuff at creation
    - culls dead stuff
    - pokes stuff to process their actions
    """

    def __init__(self, config: TSGConfig, surface: pg.Surface, cell_dims: Tuple[float, float]):
        super().__init__(config, surface, cell_dims)
        self.place_chance = self.config.stuff_chance

    def place(self):
        """
        Initial World with randomly placed Stuff
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                can_place = random.randint(0, self.config.stuff_chance)
                if can_place == self.place_chance:
                    self.add(Cell(x, y))

    def add(self, cell: Cell):
        """
        Add a new Stuff instance to the matrix
        :param row: which row
        :param col: which col
        """
        self.counter += 1
        self.matrix[cell.x][cell.y] = Stuff(self, self.surface, cell, int(self.cell_dims[0]))

    def cull(self):
        """
        Cull Stuff marked as 'dead' from the matrix
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                stuff = self.matrix[x][y]
                if stuff and stuff.dead:
                    self.remove(Cell(x, y))

    def process(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Stuff is present,
        tell it to process its actions
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                stuff = self.matrix[x][y]
                if stuff:
                    stuff.process(do_actions)
