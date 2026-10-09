"""Mutable musical note timing and expression; pitch is the mapping key."""
from dataclasses import dataclass

DEFAULT_VELOCITY = 64
DEFAULT_LIFT = 64

@dataclass
class Note:
    pos: int
    length: int
    velocity: int = DEFAULT_VELOCITY
    lift: int = DEFAULT_LIFT
