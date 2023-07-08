from typing import Tuple

import pygame as pg

from tsg import BaseTSG, Cell


class Gack(BaseTSG):
    """
    Gack!
    """

    def __init__(self, manager, surface, cell: Cell, cell_dims: Tuple[float, float]):
        super().__init__(surface, f"G{manager.counter}", cell, pg.Color(0, 0, 100))
        self.manager = manager
        self.rect = (
            cell.x * cell_dims[0],
            cell.y * cell_dims[1],
            cell_dims[0],
            cell_dims[1],
        )

    def __str__(self) -> str:
        return f"{self.name}, cell: ({self.cell}), age: {self.age}, energy: {self.energy}"

    def process(self, do_actions: bool):
        self.draw()

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.rect)
