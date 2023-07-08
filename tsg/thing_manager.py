"""
Manages the Thing instances in the World.
"""
import random
from typing import List, Tuple

import pygame as pg

from tsg import BaseManager, Cell, Thing, TSGConfig


class ThingManager(BaseManager):
    """
    Manages the Stuff instances in the World.

    - randomly places stuff at creation
    - culls dead stuff
    - pokes stuff to process their actions
    """

    def __init__(self, config: TSGConfig, surface: pg.Surface, cell_dims: Tuple[float, float]):
        super().__init__(config, surface, cell_dims)
        self.place_chance = self.config.thing_chance

    def place(self):
        """
        Initial World with randomly placed Things
        """
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                can_place = random.randint(0, self.config.thing_chance)
                if can_place == self.place_chance:
                    self.add(Cell(row, col))

    def add(self, cell: Cell):
        """
        Add a new Thing instance to the matrix
        :param row: which row
        :param col: which col
        """
        print(f"Add thing @ {cell}")
        self.counter += 1
        self.matrix[cell.x][cell.y] = Thing(self, self.surface, cell, int(self.cell_dims[0]))

    def cull(self):
        """
        Cull Stuff marked as 'dead' from the matrix
        """
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                # print(f"cull @ {row},{col}")
                tsg_thing = self.matrix[row][col]
                if tsg_thing:
                    tsg_thing.has_moved = False
                if tsg_thing and tsg_thing.dead:
                    self.remove(Cell(row, col))

    def move(self, thing: Thing, new_cell: Cell):
        # print(f"MGR.move {thing.name} from {thing.cell} to {new_cell}")
        self.remove(thing.cell)
        self.matrix[new_cell.x][new_cell.y] = thing
        thing.cell = new_cell
        self.update_position(thing)

    def update_position(self, thing: Thing):
        thing.pos = (
            (thing.tile_size * ((thing.cell.x * thing.tile_size) // thing.tile_size)) + thing.size,
            (thing.tile_size * ((thing.cell.y * thing.tile_size) // thing.tile_size)) + thing.size,
        )

    def process(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Thing is present,
        tell it to process its actions
        """
        for row in range(self.config.world_width):
            for col in range(self.config.world_height):
                # print(f"process {row},{col}")
                tsg_thing = self.matrix[row][col]
                if tsg_thing:
                    tsg_thing.process(do_actions)
