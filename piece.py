from dataclasses import dataclass
from consts import colorTuple


@dataclass
class Piece:
    color: colorTuple
    rotation: int
    x: int
    y: int
    shape: str
