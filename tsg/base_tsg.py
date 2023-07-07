"""
Base class for TSG classes.
"""
import pygame as pg

from tsg import Cell


class BaseTSG:
    """
    Base class for TSG classes.
    """

    def __init__(self, surface: pg.Surface, name: str, cell: Cell, color: pg.Color):
        self.surface = surface
        self.energy = 1
        self.age = 0
        self.lifespan = 0
        self.spawn_threshold = 0
        self.cell = cell
        self.color = color
        self.dead = False  # is this instance alive or dead
        self.name = name

    def draw(self):
        """
        Draw entity in the world.
        """

    def process(self, do_actions: bool):
        """
        Process entity actions
        """
