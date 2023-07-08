"""
Manages the placement of Gack instances in the World.
"""
import random
from typing import Tuple

import pygame as pg

from tsg import BaseManager, Cell, Gack, TSGConfig


class GackManager(BaseManager):
    """
    Manages the placement of Gack instances in the World.

    - randomly places Gack at creation
    """

    def __init__(self, config: TSGConfig, surface: pg.Surface, cell_dims: Tuple[float, float]):
        super().__init__(config, surface, cell_dims)
        self.place_chance = self.config.gack_chance
        self.cell_dims = cell_dims

    def place(self):
        """
        Initial World with randomly placed Gack
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                can_place = random.randint(0, self.config.gack_chance)
                if can_place == self.place_chance:
                    # gack is added in a block defined by `gack_size`
                    for gack_w in range(self.config.gack_size):
                        for gack_h in range(self.config.gack_size):
                            if x + gack_w < self.max_width and y + gack_h < self.max_height:
                                self.add(Cell(x + gack_w, y + gack_h))

    def add(self, cell: Cell):
        """
        Add a new Gack instance to the matrix
        :param row: which row
        :param col: which col
        """
        self.counter += 1
        self.matrix[cell.x][cell.y] = Gack(self, self.surface, cell, self.cell_dims)
