import pygame as pg

from tsg import BaseTSG, Cell, Dims


class Gack(BaseTSG):
    """
    Gack!
    """

    def __init__(self, manager, surface: pg.Surface, cell: Cell, cell_dims: Dims):
        super().__init__(
            manager, surface, f"G{manager.counters['G']}", cell, cell_dims, pg.Color(0, 0, 100)
        )
        self.rect = (
            cell.x * cell_dims.w,
            cell.y * cell_dims.h,
            cell_dims.w,
            cell_dims.h,
        )

    def process(self, do_actions: bool):
        self.draw()

    def draw(self):
        pg.draw.rect(self.surface, self.color, self.rect)
