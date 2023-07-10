"""
Type definitions used in TSG
"""
from dataclasses import dataclass


@dataclass
class Cell:
    """
    Defines a cell in the World
    """

    x: int = 0
    y: int = 0
    is_free: bool = False


@dataclass
class TSGConfig:
    """
    Config details
    """

    update_period: float
    growth_period: int
    tick_speed: int
    resolution_w: int
    resolution_h: int
    world_width: int
    world_height: int
    stuff_chance: float
    gack_chance: float
    gack_size: int
    thing_chance: float


@dataclass
class Factors:
    """
    Factors affect a Things stats and traits

    :param drift: mutation probabilty
    """

    drift: float = 0.0
    speed: float = 1.0
    spin: float = 1.0
    spawn: float = 1.0
    feed: float = 1.0
    lifespan: float = 1.0
    fission: float = 1.0
    fusion: float = 0.0
    hunger: float = 1.0
    thing: float = 0.0
    stuff: float = 1.0
    no_gack: float = 1.0
    wet_gack: float = 0.0
    dry_gack: float = 0.0


@dataclass
class Traits:
    no_gack: int = 1
    wet_gack: int = 0
    dry_gack: int = 0
    stuff: int = 1
    thing: int = 0
    fission: int = 1
    fusion: int = 1
