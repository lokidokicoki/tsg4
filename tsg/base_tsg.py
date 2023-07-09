"""
Base class for TSG classes.
"""
from typing import List, Tuple

import pygame as pg

from tsg import Cell


class BaseTSG:
    """
    Base class for TSG classes.
    """

    def __init__(
        self,
        manager,
        surface: pg.Surface,
        name: str,
        cell: Cell,
        cell_dims: Tuple[float, float],
        color: pg.Color,
    ):
        self.manager = manager
        self.surface = surface
        self.energy = 1
        self.age = 0
        self.lifespan = 0
        self.spawn_threshold = 0
        self.cell = cell
        self.color = color
        self.dead = False  # is this instance alive or dead
        self.name = name
        self.cell_dims = cell_dims
        self.pos = None
        self.size = cell_dims[0]
        self.lineage: List[str] = []

    def __str__(self) -> str:
        return (
            f"{self.name}, lineage: {'->'.join(self.lineage)} cell: ({self.cell}), "
            f"age: {self.age}, energy: {self.energy}"
        )

    def draw(self):
        """
        Draw entity in the world.
        """

    def process(self, do_actions: bool):
        """
        Process entity actions
        """
