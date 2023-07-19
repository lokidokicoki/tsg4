"""
Stuff - this grows on the substrate of the World.
It gains energy at a set rate, and will spawn new stuff in empty spaces next to it
"""
import pygame as pg

from tsg import BaseTSG, Cell, Dims


class Stuff(BaseTSG):
    """
    Create a Stuff instance at a specified point in the World
    """

    def __init__(self, manager, surface: pg.Surface, cell: Cell, cell_dims: Dims):
        super().__init__(
            manager, surface, f"S{manager.counters['S']}", cell, cell_dims, pg.Color(0, 10, 0)
        )
        self.size = cell_dims.w / 2
        self.lifespan = 100
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.update_position()

    def process(self, do_actions: bool):
        """
        Stuff does the following:
        - eat
        - spawn
        - die
        """
        super().process(do_actions)

        if do_actions:
            self.eat()
            self.spawn()
            self.die()
            self.age += 1
            self.hunger += 1

        self.draw()

    def eat(self):
        """
        'Eat' substrate and grow!
        """
        if self.hunger >= 2:
            self.energy += 1
            self.color.g = min(200, 10 * self.energy)
            self.hunger = 0

    def spawn(self):
        """
        If the instance has enough energy, attempt to spawn a new stuff
        """
        if self.energy > self.spawn_threshold:
            # check for free adjacent cellsin manager
            next_free_cell = self.manager.get_next_free_cell(self.cell, "S")

            if next_free_cell:
                self.manager.add(Stuff, next_free_cell.cell)
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
        pg.draw.circle(self.surface, self.color, (self.pos.x, self.pos.y), self.size)
