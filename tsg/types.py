"""
Type definitions used in TSG
"""
from dataclasses import dataclass


@dataclass
class Cell:
    """
    Defines a cell in the World
    """

    x: int
    y: int


@dataclass
class NextFreeCell:
    """
    Defines a cell in the World
    """

    is_free: bool
    x: int
    y: int


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
    stuff_chance: float
    gack_chance: float
    gack_size: int
    thing_chance: float
