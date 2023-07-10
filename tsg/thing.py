"""
Thing - this can eat Stuff - or other Things
It gains energy from eating, and will spawn new Things in empty spaces next to it
"""

import random
from math import cos, pi, sin
from typing import Tuple

import pygame as pg

from tsg import BaseTSG, Cell


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
        self.size = cell_dims[0] / 2
        self.lifespan = 600
        self.energy = 50
        self.spawn_threshold = 250  # amount of energy required to spawn
        self.pos = (
            (cell_dims[0] * ((cell.x * cell_dims[0]) // cell_dims[0])) + self.size,
            (cell_dims[0] * ((cell.y * cell_dims[0]) // cell_dims[0])) + self.size,
        )
        self.facing = random.randint(0, 7)
        self.eye_size = self.size * 0.1
        self.eye_color = pg.Color(200, 0, 0)
        self.has_moved = False
        self.hunger_threshold = 30

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.move()
            self.eat()
            self.spawn()
            self.die()
            self.age += 1
            self.energy -= 1
            self.hunger += 1

        self.draw()

    def move(self):
        """
        check is cell in facing direction is clear, if so move into it
        """
        if not self.has_moved:
            if self.hunger > self.hunger_threshold:
                facing_cell = self.manager.get_facing_cell(self.facing, self.cell, "S")
                if facing_cell.is_free:
                    self.facing = random.randint(0, 7)
                    self.hunger /= 5

            facing_cell = self.manager.get_facing_cell(self.facing, self.cell, "T")
            if facing_cell.is_free:
                facing_cell = self.manager.get_facing_cell(self.facing, self.cell, "G")

            if facing_cell.is_free:
                self.manager.move(self, facing_cell)
            else:
                self.facing = random.randint(0, 7)
            self.has_moved = True

    def eat(self):
        """
        Eat Stuff!
        """
        stuff = self.manager.matrix[self.cell.x][self.cell.y].get("S")

        if stuff:
            free_energy = stuff.energy - 1
            self.energy += free_energy
            self.hunger = 0
            stuff.energy = 1

    def spawn(self):
        """
        Spawn a new Thing - simple fission
        """
        if self.energy >= self.spawn_threshold:
            next_free_cell = self.manager.get_next_free_cell(self.cell, "T")

            if next_free_cell.is_free:
                new_thing = self.manager.add(Thing, next_free_cell)
                new_thing.lineage = self.lineage.copy()
                new_thing.lineage.append(self.name)
                self.manager.lineages.add((self.name, new_thing.name))
                self.energy = self.energy / 2

    def die(self, force: bool = False):
        """
        If lifespan reached, or energy all gone, the Thing dies.
        """
        if force or self.age > self.lifespan or self.energy <= 0:
            self.dead = True

        if self.dead:
            self.color = pg.Color(255, 255, 0)

    def draw(self):
        draw_regular_polygon(self.surface, self.color, 8, self.size, self.pos)
        draw_eye_spot(
            self.surface, self.eye_color, 8, self.facing, self.size, self.eye_size, self.pos
        )
