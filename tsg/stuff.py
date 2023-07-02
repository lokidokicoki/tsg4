import pygame as pg

from tsg import BaseTSG


class Stuff(BaseTSG):
    """
    Stuff - this grows on the substrate of the World.
    It gains energy at a set rate, and will spawn new stuff in empty spaces next to it
    """

    def __init__(self, manager, surface, row: int, col: int, size: int):
        super().__init__(surface, f"S{manager.counter}", row, col, pg.Color(0, 10, 0))
        self.manager = manager
        self.size = size / 2
        self.lifespan = 50
        self.spawn_threshold = 20  # amount of energy required to spawn
        self.pos = (
            (size * ((row * size) // size)) + self.size,
            (size * ((col * size) // size)) + self.size,
        )

    def __str__(self) -> str:
        return f"{self.name}, cell: ({self.row},{self.col}), age: {self.age}, energy: {self.energy}"

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.eat()
            self.spawn()
            self.die()

        self.draw()

    def eat(self):
        self.energy += 1
        self.age += 1
        self.color.g = min(200, 10 * self.energy)

    def spawn(self):
        # spawn a new stuff
        if self.energy > self.spawn_threshold:
            # check for free adjacent squares in manager
            has_free_cell, row, col = self.manager.get_next_free_cell(self.row, self.col)

            if has_free_cell:
                self.manager.add(row, col)
                self.energy = int(self.energy / 2)
            else:
                self.die(True)

    def die(self, force: bool = False):
        if force or self.age > self.lifespan:
            self.dead = True

        if self.dead:
            self.color = pg.Color(255, 0, 0)

    def draw(self):
        pg.draw.circle(self.surface, self.color, self.pos, self.size)
