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
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                can_place = random.randint(0, self.config.gack_chance)
                if can_place == self.place_chance:
                    # gack is added in a block defined by `gack_size`
                    for gack_row in range(self.config.gack_size):
                        for gack_col in range(self.config.gack_size):
                            if row + gack_row < self.wlim and col + gack_col < self.hlim:
                                self.add(Cell(row + gack_row, col + gack_col))

    def add(self, cell: Cell):
        """
        Add a new Gack instance to the matrix
        :param row: which row
        :param col: which col
        """
        self.counter += 1
        self.matrix[cell.row][cell.col] = Gack(self, self.surface, cell, self.cell_dims)
