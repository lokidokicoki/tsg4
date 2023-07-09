"""
Stuff - this grows on the substrate of the World.
It gains energy at a set rate, and will spawn new stuff in empty spaces next to it
"""

from typing import Tuple

import pygame as pg

from tsg import BaseTSG, Cell


class Stuff(BaseTSG):
    """
    Create a Stuff instance at a specified point in the World
    """

    def __init__(self, manager, surface, cell: Cell, cell_dims: Tuple[float, float]):
        super().__init__(
            manager, surface, f"S{manager.counters['S']}", cell, cell_dims, pg.Color(0, 10, 0)
        )
        self.manager = manager
        self.size = cell_dims[0] / 2
        self.lifespan = 50
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.pos = (
            (cell_dims[0] * ((cell.x * cell_dims[0]) // cell_dims[0])) + self.size,
            (cell_dims[0] * ((cell.y * cell_dims[0]) // cell_dims[0])) + self.size,
        )

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.eat()
            self.spawn()
            self.die()
            self.age += 1

        self.draw()

    def eat(self):
        """
        'Eat' substrate and grow!
        """
        self.energy += 1
        self.color.g = min(200, 10 * self.energy)

    def spawn(self):
        """
        If the instance has enough energy, attempt to spawn a new stuff
        """
        if self.energy > self.spawn_threshold:
            # check for free adjacent cellsin manager
            next_free_cell = self.manager.get_next_free_cell(self.cell, "S")

            if next_free_cell.is_free:
                self.manager.add(Stuff, next_free_cell)
                self.energy = int(self.energy / 2)
            else:
                self.die(True)

    def die(self, force: bool = False):
        """
        You died
        """
        if self.manager.matrix[self.cell.x][self.cell.y].get("G") is not None:
            self.dead = True
        if force or self.age > self.lifespan:
            self.dead = True

        if self.dead:
            self.color = pg.Color(255, 0, 0)

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.pos, self.size)
