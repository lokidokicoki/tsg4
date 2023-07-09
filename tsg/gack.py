from typing import Tuple

import pygame as pg

from tsg import BaseTSG, Cell


class Gack(BaseTSG):
    """
    Gack!
    """

    def __init__(self, manager, surface, cell: Cell, cell_dims: Tuple[float, float]):
        super().__init__(
            manager, surface, f"G{manager.counters['G']}", cell, cell_dims, pg.Color(0, 0, 100)
        )
        self.rect = (
            cell.x * cell_dims[0],
            cell.y * cell_dims[1],
            cell_dims[0],
            cell_dims[1],
        )

    def process(self, do_actions: bool):
        self.draw()

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.rect)
