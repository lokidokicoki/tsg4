"""
World - This looks after the various entities in the World
"""
import random
from typing import List, Optional, Tuple, Type, Union

import pygame as pg

from tsg import Cell, Gack, Stuff, Thing, TSGConfig


class CellContent:
    """
    What is going on in a cell or the World grid
    """

    def __init__(self, cell: Cell):
        self.thing: Optional[Thing] = None
        self.stuff: Optional[Stuff] = None
        self.gack: Optional[Gack] = None
        self.cell = cell

    def set(self, entity: Union[Thing, Stuff, Gack]):
        """
        Set the contents of a grid cell
        """
        if isinstance(entity, Thing):
            self.thing = entity
        elif isinstance(entity, Stuff):
            self.stuff = entity
        elif isinstance(entity, Gack):
            self.gack = entity
        else:
            raise TypeError(f"Uknown entity type {entity}")

    def get(self, check_type: str):
        """
        Get the specific entity in a grid cell
        """
        match check_type:
            case "T":
                return self.thing
            case "S":
                return self.stuff
            case "G":
                return self.gack

    def remove(self, check_type: str):
        """
        Clear the specific entity in this grid cell
        """
        match check_type:
            case "T":
                self.thing = None
            case "S":
                self.stuff = None
            case "G":
                self.gack = None


class World:
    """
    Manage all TSG instances
    """

    def __init__(self, config: TSGConfig, surface: pg.Surface, cell_dims: Tuple[float, float]):
        self.counters = {
            "T": 0,
            "S": 0,
            "G": 0,
        }
        self.stats = {
            "T": 0,
            "S": 0,
            "G": 0,
        }
        self.config = config
        self.surface = surface
        self.cell_dims = cell_dims
        self.matrix: List[List[CellContent]] = [
            [CellContent(Cell(row, col)) for col in range(self.config.world_height)]
            for row in range(self.config.world_width)
        ]
        self.max_width = len(self.matrix)
        self.max_height = len(self.matrix[0])

    def get_next_free_cell(self, cell: Cell, check_type: str) -> Cell:
        """
        Find the next empty cell in the matrix starting mid left and moving clockwise
        """
        next_free_cell = Cell(cell.x, cell.y)
        for direction in range(0, 7):
            next_free_cell = self.get_facing_cell(direction, cell, check_type)
            if next_free_cell.is_free:
                break

        return next_free_cell

    def get_facing_cell(self, facing_direction: int, cell: Cell, check_type: str) -> Cell:
        """
        Translate facing to Cell, facing dir is 0 to 7 from right CW
        """
        x = cell.x
        y = cell.y
        match facing_direction:
            case 0:
                x += 1
            case 1:
                x += 1
                y += 1
            case 2:
                y += 1
            case 3:
                x -= 1
                y += 1
            case 4:
                x -= 1
            case 5:
                x -= 1
                y -= 1
            case 6:
                y -= 1
            case 7:
                x += 1
                y -= 1

        if (
            0 <= x < self.max_width
            and 0 <= y < self.max_height
            and self.matrix[x][y].get(check_type) is None
        ):
            return Cell(x, y, True)

        return Cell(cell.x, cell.y, False)

    def add(self, klass: Union[Type[Gack], Type[Thing], Type[Stuff]], cell: Cell):
        """
        Add entity to World at specified row and column
        """

        entity = klass(self, self.surface, cell, self.cell_dims)
        if isinstance(entity, Thing):
            self.counters["T"] += 1
            self.stats["T"] += 1
        elif isinstance(entity, Stuff):
            self.counters["S"] += 1
            self.stats["S"] += 1
        elif isinstance(entity, Gack):
            self.counters["G"] += 1
            self.stats["G"] += 1
        else:
            raise TypeError(f"Uknown entity type {entity}")

        self.matrix[cell.x][cell.y].set(entity)
        return entity

    def cull(self):
        """
        Cull entities in the World.

        This flags them for later removal.
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                cell_content = self.matrix[x][y]
                if cell_content.stuff and cell_content.stuff.dead:
                    cell_content.stuff = None
                    self.stats["S"] -= 1
                if cell_content.thing:
                    cell_content.thing.has_moved = False
                    if cell_content.thing.dead:
                        cell_content.thing = None
                        self.stats["T"] -= 1

    def process(self, do_actions: bool = False):
        """
        Check each cell in matrix, if a Stuff is present,
        tell it to process its actions
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                cell_content = self.matrix[x][y]
                if cell_content.gack:
                    cell_content.gack.process(do_actions)
                if cell_content.stuff:
                    cell_content.stuff.process(do_actions)
                if cell_content.thing:
                    cell_content.thing.process(do_actions)

    def remove(self, cell: Cell, check_type: str):
        """
        Remove TSG instance from matrix
        """
        self.matrix[cell.x][cell.y].remove(check_type)

    def growth_season(self):
        """
        Initial World with randomly placed entities
        """
        print("GROWTH_SEASON")

        for x in range(self.max_width):
            for y in range(self.max_height):
                can_place = random.uniform(0, 1)
                if can_place <= self.config.stuff_chance / 10:
                    self.add(Stuff, Cell(x, y))

    def place(self):
        """
        Initial World with randomly placed entities
        """
        for x in range(self.max_width):
            for y in range(self.max_height):
                can_place = random.uniform(0, 1)
                if can_place <= self.config.gack_chance:
                    self._add_gack(x, y)

                if can_place <= self.config.stuff_chance:
                    self.add(Stuff, Cell(x, y))

                if can_place <= self.config.thing_chance:
                    self.add(Thing, Cell(x, y))

    def move(self, thing: Thing, new_cell: Cell):
        """
        Move a Thing to a new cell
        """
        self.remove(thing.cell, "T")
        self.matrix[new_cell.x][new_cell.y].set(thing)
        thing.cell = new_cell
        self.update_position(thing)

    def update_position(self, klass: Union[Thing, Stuff, Gack]):
        """
        Update the on screen positioin of a Thing
        """
        klass.pos = (
            (klass.cell_dims[0] * ((klass.cell.x * klass.cell_dims[0]) // klass.cell_dims[0]))
            + klass.size,
            (klass.cell_dims[1] * ((klass.cell.y * klass.cell_dims[1]) // klass.cell_dims[1]))
            + klass.size,
        )

    def get_grid_at_pos(self, target) -> Cell:
        """
        Translate mouse position to a grid cell
        """
        x = self.cell_dims[0] * (target[0] // self.cell_dims[0])
        y = self.cell_dims[1] * (target[1] // self.cell_dims[1])

        if x > 0:
            x /= self.cell_dims[0]
        if y > 0:
            y /= self.cell_dims[1]
        target_cell = Cell(int(x), int(y))
        return target_cell

    def dump_cell_contents(self, target):
        """
        Output cell contents at mouse position
        """
        cell = self.get_grid_at_pos(target)
        contents = self.matrix[cell.x][cell.y]

        print(f"Cell contents @ {cell}")
        if contents.thing:
            print(f"=> Thing {contents.thing}")
        if contents.stuff:
            print(f"=> Stuff {contents.stuff}")
        if contents.gack:
            print(f"=> Gack  {contents.gack}")
        print("---")

    def _add_gack(self, x: int, y: int):
        # gack is added in a block defined by `gack_size`
        for gack_w in range(self.config.gack_size):
            for gack_h in range(self.config.gack_size):
                if x + gack_w < self.max_width and y + gack_h < self.max_height:
                    self.add(Gack, Cell(x + gack_w, y + gack_h))
