"""
Thing - this can eat Stuff - or other Things
It gains energy from eating, and will spawn new Things in empty spaces next to it
"""

import random
from math import cos, pi, sin
from typing import Tuple

import pygame as pg

from tsg import BaseTSG, Cell, NextFreeCell


def draw_eye_spot(surface, color, vertex_count, facing, radius, eye_radius, position):
    x, y = position
    n, r = vertex_count, radius

    pos = (x + r * cos(2 * pi * facing / n), y + r * sin(2 * pi * facing / n))
    pg.draw.circle(surface, color, pos, eye_radius)


def draw_regular_polygon(surface, color, vertex_count, radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pg.draw.polygon(
        surface,
        color,
        [(x + r * cos(2 * pi * i / n), y + r * sin(2 * pi * i / n)) for i in range(n)],
        width,
    )


class Thing(BaseTSG):
    """
    Create a Thing instance at a specified point in the World
    """

    def __init__(self, manager, surface, cell: Cell, cell_dims: Tuple[float, float]):
        super().__init__(
            manager, surface, f"T{manager.counters['T']}", cell, cell_dims, pg.Color(100, 100, 100)
        )
        self.manager = manager
        self.size = cell_dims[0] / 2
        self.lifespan = 50
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.pos = (
            (cell_dims[0] * ((cell.x * cell_dims[0]) // cell_dims[0])) + self.size,
            (cell_dims[0] * ((cell.y * cell_dims[0]) // cell_dims[0])) + self.size,
        )
        self.facing = 0  #  random.randint(0, 7)
        self.eye_size = self.size * 0.1
        self.eye_color = pg.Color(200, 0, 0)
        self.has_moved = False

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.move()
            self.eat()
            self.spawn()
            self.die()

        self.draw()

    def move(self):
        """
        check is cell in facing direction is clear, if so move into it
        """
        if not self.has_moved:
            # print(f"Pre move {self.name}: facing {self.facing}, c:{self.cell}")
            facing_cell = self.manager.get_facing_cell(self.facing, self.cell, "T")
            # print(f" => move to - facing cell {facing_cell}")
            if facing_cell.is_free:
                self.manager.move(self, facing_cell)
            else:
                self.facing = random.randint(0, 7)
            self.has_moved = True
            # print(f"=> matrix post move {self.manager.matrix}")

    def eat(self):
        pass

    def spawn(self):
        pass

    def die(self):
        pass

    def draw(self):
        draw_regular_polygon(self.surface, self.color, 8, self.size, self.pos)
        draw_eye_spot(
            self.surface, self.eye_color, 8, self.facing, self.size, self.eye_size, self.pos
        )
