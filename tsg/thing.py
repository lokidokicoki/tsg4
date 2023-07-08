"""
Thing - this can eat Stuff - or other Things
It gains energy from eating, and will spawn new Things in empty spaces next to it
"""

import random
from math import cos, pi, sin

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

    def __init__(self, manager, surface, cell: Cell, size: int):
        super().__init__(surface, f"T{manager.counter}", cell, pg.Color(100, 100, 100))
        self.manager = manager
        self.size = size / 2
        self.tile_size = size
        self.lifespan = 50
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.pos = (
            (size * ((cell.x * size) // size)) + self.size,
            (size * ((cell.y * size) // size)) + self.size,
        )
        self.facing = 3  # random.randint(0, 7)
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
        if not self.has_moved:
            # check is cell in facing direction is clear, if so move into it

            print(f"Pre move {self.name}:f {self.facing}, c:{self.cell}")
            facing_cell = self.manager.get_facing_cell(self.facing, self.cell)
            print(f" => move to - facing cell {facing_cell}")
            if facing_cell.is_free:
                self.manager.move(self, facing_cell)
            else:
                self.facing = random.randint(0, 7)
            self.has_moved = True
            print(f"matrix post move {self.manager.matrix}")

    def eat(self):
        pass

    def spawn(self):
        pass

    def die(self):
        pass

    def draw(self):
        draw_regular_polygon(self.surface, self.color, 8, self.size, self.pos)
        # pg.draw.circle(self.surface, self.color, self.pos, self.size)
        draw_eye_spot(
            self.surface, self.eye_color, 8, self.facing, self.size, self.eye_size, self.pos
        )
