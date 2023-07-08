"""
BaseManager - This looks after the various entities in the World

The BaseManager is subclassed for the spefici entity types.
"""
from typing import List, Optional, Tuple

import pygame as pg

from tsg import BaseTSG, Cell, NextFreeCell, TSGConfig


class BaseManager:
    """
    Base Maanger for TSG instances
    """

    def __init__(self, config: TSGConfig, surface: pg.Surface, cell_dims: Tuple[float, float]):
        self.counter = 0
        self.config = config
        self.surface = surface
        self.cell_dims = cell_dims
        self.matrix: List[List[Optional[BaseTSG]]] = [
            [None for col in range(self.config.world_height)]
            for row in range(self.config.world_width)
        ]
        self.max_width = len(self.matrix)
        self.max_height = len(self.matrix[0])

    def get_next_free_cell(self, cell: Cell) -> NextFreeCell:
        """
        Find the next empty cell in the matrix starting mid left and moving clockwise
        """
        next_free_cell = NextFreeCell(False, cell.x, cell.y)
        for direction in range(0, 7):
            next_free_cell = self.get_facing_cell(direction, cell)
            if next_free_cell.is_free:
                break

        return next_free_cell

    def get_facing_cell(self, facing_direction: int, cell: Cell) -> NextFreeCell:
        """
        Translate facing to Cell, facing dir is 0 to 7 from right CW
        """
        x = cell.x
        y = cell.y
        match facing_direction:
            case 0:
                x += 1
            case 1:
                x += 1
                y += 1
            case 2:
                y += 1
            case 3:
                x -= 1
                y += 1
            case 4:
                x -= 1
            case 5:
                x -= 1
                y -= 1
            case 6:
                y -= 1
            case 7:
                x += 1
                y -= 1

        if 0 <= x < self.max_width and 0 <= y < self.max_height and self.matrix[x][y] is None:
            return NextFreeCell(True, x, y)

        return NextFreeCell(False, cell.x, cell.y)

    def add(self, cell: Cell):
        """
        Add entity to World at specified row and column
        """

    def cull(self):
        """
        Cull entities in the World.

        This flags them for later removal.
        """

    def process(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Stuff is present,
        tell it to process its actions
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                tsg = self.matrix[x][y]
                if tsg:
                    tsg.process(do_actions)

    def remove(self, cell: Cell):
        """
        Remove TSG instance from matrix
        """
        self.matrix[cell.x][cell.y] = None
