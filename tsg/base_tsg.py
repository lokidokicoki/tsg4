"""
Base class for TSG classes.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple

import pygame as pg

from tsg import Cell


class BaseTSG(ABC):
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
        self.pos = (0, 0)
        self.size = cell_dims[0]
        self.lineage: List[str] = []
        self.hunger = 0

    def __str__(self) -> str:
        return (
            f"{self.name}, lineage: {'->'.join(self.lineage)} cell: ({self.cell}), "
            f"age: {self.age}, energy: {self.energy}"
        )

    @abstractmethod
    def draw(self):
        """
        Draw entity in the world.
        """

    @abstractmethod
    def process(self, do_actions: bool):
        """
        Process entity actions
        """

    def update_position(self):
        """
        Update the on screen positioin of a Thing
        """
        self.pos = (
            (self.cell_dims[0] * ((self.cell.x * self.cell_dims[0]) // self.cell_dims[0]))
            + self.size,
            (self.cell_dims[1] * ((self.cell.y * self.cell_dims[1]) // self.cell_dims[1]))
            + self.size,
        )
