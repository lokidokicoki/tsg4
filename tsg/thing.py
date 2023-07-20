"""
Thing - this can eat Stuff - or other Things
It gains energy from eating, and will spawn new Things in empty spaces next to it
"""

import dataclasses
import random
from math import cos, pi, sin

import pygame as pg

from tsg import BaseTSG, Cell, Dims, Factors, GeneType, Genome, Point, Traits


def draw_eye_spot(
    surface: pg.Surface,
    color: pg.Color,
    vertex_count: int,
    facing: int,
    radius: float,
    eye_radius: float,
    position: Point,
):
    """
    Draw eye spot indicating direction the Thing is facing
    """
    pos = (
        position.x + radius * cos(2 * pi * facing / vertex_count),
        position.y + radius * sin(2 * pi * facing / vertex_count),
    )
    pg.draw.circle(surface, color, pos, eye_radius)


def draw_regular_polygon(
    surface: pg.Surface,
    color: pg.Color,
    vertex_count: int,
    radius: float,
    position: Point,
    width=0,
):
    """
    Draw a regular polygon.
    """
    pg.draw.polygon(
        surface,
        color,
        [
            (
                position.x + radius * cos(2 * pi * i / vertex_count),
                position.y + radius * sin(2 * pi * i / vertex_count),
            )
            for i in range(vertex_count)
        ],
        width,
    )


class Thing(BaseTSG):
    """
    Create a Thing instance at a specified point in the World
    """

    def __init__(self, manager, surface: pg.Surface, cell: Cell, cell_dims: Dims):
        super().__init__(
            manager, surface, f"T{manager.counters['T']}", cell, cell_dims, pg.Color(100, 100, 100)
        )
        self.size = cell_dims.w / 2
        self.update_position()
        self.lifespan = 600
        self.energy = 50
        self.spawn_threshold = 250  # amount of energy required to spawn
        self.facing = random.randint(0, 7)
        self.eye_size = self.size * 0.1
        self.eye_color = pg.Color(200, 0, 0)
        self.has_moved = False
        self.hunger_threshold = 30
        self.speed = 1
        self.factors = Factors()
        self.traits = Traits()
        self.genome = Genome()

    def process(self, do_actions: bool):
        super().process(do_actions)

        if do_actions:
            self.move()
            self.spin()
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
            speed_gene = self.genome.get_gene_by_type(GeneType.SPEED)
            facing_cell = self.manager.get_facing_cell(self.facing, self.cell)  # , "S")

            if facing_cell:
                if facing_cell.is_empty and self.hungry():
                    self.spin()
                    self.hunger /= 5
                elif facing_cell.get("T") or facing_cell.get("G"):
                    self.spin()
                else:
                    self.manager.move(self, facing_cell.cell)
                    self.has_moved = True

    def hungry(self):
        hunger_gene = self.genome.get_gene_by_type(GeneType.HUNGER)
        return self.hunger > self.hunger_threshold * hunger_gene.get_weight_as_float()

    def spin(self):
        if not self.has_moved:
            spin_rate_gene = self.genome.get_gene_by_type(GeneType.SPIN_RATE)
            spin_cw_gene = self.genome.get_gene_by_type(GeneType.SPIN_CW)
            spin_ccw_gene = self.genome.get_gene_by_type(GeneType.SPIN_CCW)
            max_spin = int(7 * spin_rate_gene.get_weight_as_float())

            direction = random.random()
            if direction < spin_cw_gene.get_weight_as_float():
                self.facing = (self.facing + random.randint(0, max_spin)) % 8
            elif direction < spin_ccw_gene.get_weight_as_float():
                self.facing = (self.facing - random.randint(0, max_spin)) + 8

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
        if self.energy >= self.spawn_threshold * self.factors.spawn:
            next_free_cell = self.manager.get_next_free_cell(self.cell, "T")

            if next_free_cell:
                new_thing = self.manager.add(Thing, next_free_cell.cell)
                new_thing.lineage = self.lineage.copy()
                new_thing.lineage.append(self.name)
                self.manager.lineages.add((self.name, new_thing.name))
                self.energy = self.energy / 2

                # set up factors
                self.mutate(self, new_thing, self.manager.config.mutation_rate)

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

    @staticmethod
    def mutate(parent, child, mutation_rate, force=False):
        """
        Mutate child factors at given rate
        """
        # copy parent factors to child
        for idx, gene in enumerate(parent.genome.genes):
            child.genome.genes[idx].weight = gene.weight

            if mutation_rate <= random.random():
                rand_gene = child.genome.genes[random.randint(0, len(child.genome.genes) - 1)]
                rand_gene.weight = rand_gene.weight ^ random.randint(0, 0xFF)
                print(rand_gene)

        values = child.genome.get_genotype()
        print(values)
        child.color = pg.Color(values[0], values[1], values[2])
