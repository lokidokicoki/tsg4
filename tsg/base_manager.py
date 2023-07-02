from typing import List, Optional, Tuple

import pygame as pg

from tsg import BaseTSG, TSGConfig


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
            [None for col in range(self.config.world_width)]
            for row in range(self.config.world_height)
        ]
        self.wlim = len(self.matrix)
        self.hlim = len(self.matrix[0])

    def get_next_free_cell(self, row, col) -> Tuple[bool, int, int]:
        """
        Find the next empty cell in the matrix starting top left and moving clockwise
        """
        # check adjacent cells to passed row and col
        if (row - 1 >= 0) and (col - 1 >= 0) and self.matrix[row - 1][col - 1] is None:
            return (True, row - 1, col - 1)
        if (row - 1 >= 0) and self.matrix[row - 1][col] is None:
            return (True, row - 1, col)
        if (
            (row - 1 >= 0)
            and (col + 1 < self.config.world_height)
            and self.matrix[row - 1][col + 1] is None
        ):
            return (True, row - 1, col + 1)

        if (col - 1 >= 0) and self.matrix[row][col - 1] is None:
            return (True, row, col - 1)
        if (col + 1 < self.config.world_height) and self.matrix[row][col + 1] is None:
            return (True, row, col + 1)

        if (
            (row + 1 < self.config.world_width)
            and (col - 1 >= 0)
            and self.matrix[row + 1][col - 1] is None
        ):
            return (True, row + 1, col - 1)
        if (row + 1 < self.config.world_width) and self.matrix[row + 1][col] is None:
            return (True, row + 1, col)
        if (
            (row + 1 < self.config.world_width)
            and (col + 1 < self.config.world_height)
            and self.matrix[row + 1][col + 1] is None
        ):
            return (True, row + 1, col + 1)

        return (False, row, col)

    def add(self, row: int, col: int):
        pass

    def cull(self, row: int, col: int):
        pass

    def process(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Stuff is present,
        tell it to process its actions
        """
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                tsg = self.matrix[row][col]
                if tsg:
                    tsg.process(do_actions)

    def remove(self, row: int, col: int):
        """
        Remove TSG instance from matrix
        """
        self.matrix[row][col] = None
