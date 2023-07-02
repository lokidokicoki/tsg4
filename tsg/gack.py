from typing import Tuple

import pygame as pg

from tsg import BaseTSG


class Gack(BaseTSG):
    """
    Gack!
    """

    def __init__(self, manager, surface, row: int, col: int, cell_dims: Tuple[float, float]):
        super().__init__(surface, f"G{manager.counter}", row, col, pg.Color(0, 0, 100))
        self.manager = manager
        self.rect = (
            row * cell_dims[0],
            col * cell_dims[1],
            cell_dims[0],
            cell_dims[1],
        )

    def __str__(self) -> str:
        return f"{self.name}, cell: ({self.row},{self.col}), age: {self.age}, energy: {self.energy}"

    def process(self, do_actions: bool):
        self.draw()

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.rect)
