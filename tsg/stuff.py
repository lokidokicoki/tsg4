"""
Stuff - this grows on the substrate of the World.
It gains energy at a set rate, and will spawn new stuff in empty spaces next to it
"""

import pygame as pg

from tsg import BaseTSG, Cell


class Stuff(BaseTSG):
    """
    Create a Stuff instance at a specified point in the World
    """

    def __init__(self, manager, surface, cell: Cell, size: int):
        super().__init__(surface, f"S{manager.counter}", cell, pg.Color(0, 10, 0))
        self.manager = manager
        self.size = size / 2
        self.lifespan = 50
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.pos = (
            (size * ((cell.row * size) // size)) + self.size,
            (size * ((cell.col * size) // size)) + self.size,
        )

    def __str__(self) -> str:
        return f"{self.name}, cell: ({self.cell}), age: {self.age}, energy: {self.energy}"

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.eat()
            self.spawn()
            self.die()

        self.draw()

    def eat(self):
        """
        'Eat' substrate and grow!
        """
        self.energy += 1
        self.age += 1
        self.color.g = min(200, 10 * self.energy)

    def spawn(self):
        """
        If the instance has enough energy, attempt to spawn a new stuff
        """
        if self.energy > self.spawn_threshold:
            # check for free adjacent cellsin manager
            next_free_cell = self.manager.get_next_free_cell(self.cell)

            if next_free_cell.is_free:
                self.manager.add(next_free_cell.row, next_free_cell.col)
                self.energy = int(self.energy / 2)
            else:
                self.die(True)

    def die(self, force: bool = False):
        """
        You died
        """
        if force or self.age > self.lifespan:
            self.dead = True

        if self.dead:
            self.color = pg.Color(255, 0, 0)

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.pos, self.size)
