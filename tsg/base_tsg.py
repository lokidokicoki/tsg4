import pygame as pg


class BaseTSG:
    """
    Base class for TSG classes.
    """

    def __init__(self, surface: pg.Surface, name: str, row: int, col: int, color: pg.Color):
        self.surface = surface
        self.energy = 1
        self.age = 0
        self.lifespan = 0
        self.spawn_threshold = 0
        self.row = row
        self.col = col
        self.color = color
        self.dead = False  # is this instnace alive or dead
        self.name = name

    def draw(self):
        pass

    def process(self, do_actions: bool):
        pass
