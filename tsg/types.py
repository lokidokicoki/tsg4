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
