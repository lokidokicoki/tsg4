"""
Type definitions used in TSG
"""
from dataclasses import dataclass


@dataclass
class Cell:
    """
    Defines a cell in the World
    """

    row: int
    col: int


@dataclass
class TSGConfig:
    """
    Config details
    """

    update_period: float
    tick_speed: int
    resolution_w: int
    resolution_h: int
    world_width: int
    world_height: int
    stuff_chance: int
    gack_chance: int
    gack_size: int
    thing_chance: int
