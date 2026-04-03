"""Environment model for the Wumpus World."""

from __future__ import annotations

from dataclasses import dataclass

from .layouts import Coord, WumpusLayout, sort_coords


@dataclass(frozen=True, slots=True)
class Percept:
    """The local clues available in a square."""

    breeze: bool = False
    stench: bool = False

    def to_dict(self) -> dict[str, bool]:
        return {"breeze": self.breeze, "stench": self.stench}


class WumpusWorld:
    """Truth model of the world. The agent never reads hazards directly."""

    def __init__(self, layout: WumpusLayout) -> None:
        self.layout = layout
        self.size = layout.size
        self.start = layout.start
        self.pits = set(layout.pits)
        self.wumpus = layout.wumpus

    def cells(self) -> list[Coord]:
        return self.layout.cells()

    def in_bounds(self, coord: Coord) -> bool:
        row, col = coord
        return 0 <= row < self.size and 0 <= col < self.size

    def adjacent(self, coord: Coord) -> list[Coord]:
        row, col = coord
        neighbors = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]
        return sort_coords([neighbor for neighbor in neighbors if self.in_bounds(neighbor)])

    def has_pit(self, coord: Coord) -> bool:
        return coord in self.pits

    def has_wumpus(self, coord: Coord) -> bool:
        return coord == self.wumpus

    def is_hazard(self, coord: Coord) -> bool:
        return self.has_pit(coord) or self.has_wumpus(coord)

    def is_safe(self, coord: Coord) -> bool:
        return not self.is_hazard(coord)

    def safe_cells(self) -> set[Coord]:
        return {coord for coord in self.cells() if self.is_safe(coord)}

    def perceive(self, coord: Coord) -> Percept:
        if not self.in_bounds(coord):
            raise ValueError(f"Coordinate {coord} is outside the board.")

        adjacent = self.adjacent(coord)
        return Percept(
            breeze=any(square in self.pits for square in adjacent),
            stench=any(square == self.wumpus for square in adjacent),
        )
