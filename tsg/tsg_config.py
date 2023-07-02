from dataclasses import dataclass


@dataclass
class TSGConfig:
    update_period: float
    tick_speed: int
    resolution_w: int
    resolution_h: int
    world_width: int
    world_height: int
    stuff_chance: int
    gack_chance: int
    gack_size: int
