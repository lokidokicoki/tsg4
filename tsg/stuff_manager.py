"""
Manages the Stuff instances in the World.
"""
import random
from typing import List, Tuple

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
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                can_place = random.randint(0, self.config.stuff_chance)
                if can_place == self.place_chance:
                    self.add(Cell(row, col))

    def add(self, cell: Cell):
        """
        Add a new Stuff instance to the matrix
        :param row: which row
        :param col: which col
        """
        self.counter += 1
        self.matrix[cell.row][cell.col] = Stuff(self, self.surface, cell, int(self.cell_dims[0]))

    def cull(self):
        """
        Cull Stuff marked as 'dead' from the matrix
        """
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                stuff = self.matrix[row][col]
                if stuff and stuff.dead:
                    self.remove(Cell(row, col))

    def process(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Stuff is present,
        tell it to process its actions
        """
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                stuff = self.matrix[row][col]
                if stuff:
                    stuff.process(do_actions)
