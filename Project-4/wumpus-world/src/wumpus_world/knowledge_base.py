"""Explicit fact store and inference rules for the Wumpus World agent."""

from __future__ import annotations

from .environment import Percept
from .layouts import Coord, sort_coords


def _coord_to_json(coord: Coord | None) -> list[int] | None:
    return None if coord is None else [coord[0], coord[1]]


def _coords_to_json(coords: set[Coord]) -> list[list[int]]:
    return [[row, col] for row, col in sort_coords(coords)]


class WumpusKnowledgeBase:
    """Stores facts and applies the required forward-chaining rules."""

    def __init__(self, size: int, start: Coord) -> None:
        self.size = size
        self.start = start

        self.visited: set[Coord] = set()
        self.safe: set[Coord] = {start}

        self.breezy: set[Coord] = set()
        self.no_breeze: set[Coord] = set()
        self.stenchy: set[Coord] = set()
        self.no_stench: set[Coord] = set()

        self.no_pit: set[Coord] = {start}
        self.no_wumpus: set[Coord] = {start}
        self.known_pits: set[Coord] = set()
        self.known_wumpus: Coord | None = None

        self.possible_pits: set[Coord] = set()
        self.possible_wumpus: set[Coord] = set()

        self.percepts: dict[Coord, Percept] = {}
        self.inference_rounds = 0

    def cells(self) -> list[Coord]:
        return [(row, col) for row in range(self.size) for col in range(self.size)]

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

    @property
    def known_unsafe(self) -> set[Coord]:
        hazards = set(self.known_pits)
        if self.known_wumpus is not None:
            hazards.add(self.known_wumpus)
        return hazards

    def tell_percept(self, coord: Coord, percept: Percept) -> None:
        """Add a new percept and close under inference rules."""
        self.visited.add(coord)
        self.safe.add(coord)
        self.no_pit.add(coord)
        self.no_wumpus.add(coord)
        self.percepts[coord] = percept

        if percept.breeze:
            self.breezy.add(coord)
            self.no_breeze.discard(coord)
        else:
            self.no_breeze.add(coord)
            self.breezy.discard(coord)

        if percept.stench:
            self.stenchy.add(coord)
            self.no_stench.discard(coord)
        else:
            self.no_stench.add(coord)
            self.stenchy.discard(coord)

        self._apply_inference()

    def classify_square(self, coord: Coord) -> str:
        if coord in self.known_unsafe:
            return "unsafe"
        if coord in self.safe:
            return "safe"
        return "unknown"

    def adjacent_statuses(self, coord: Coord) -> list[dict[str, object]]:
        statuses = []
        for neighbor in self.adjacent(coord):
            statuses.append(
                {
                    "position": [neighbor[0], neighbor[1]],
                    "status": self.classify_square(neighbor),
                }
            )
        return statuses

    def frontier_safe(self) -> set[Coord]:
        return self.safe - self.visited

    def fact_summary(self) -> dict[str, object]:
        return {
            "visited": _coords_to_json(self.visited),
            "safe": _coords_to_json(self.safe),
            "frontier_safe": _coords_to_json(self.frontier_safe()),
            "known_pits": _coords_to_json(self.known_pits),
            "known_wumpus": _coord_to_json(self.known_wumpus),
            "possible_pits": _coords_to_json(self.possible_pits),
            "possible_wumpus": _coords_to_json(self.possible_wumpus),
            "no_pit": _coords_to_json(self.no_pit),
            "no_wumpus": _coords_to_json(self.no_wumpus),
            "breezy": _coords_to_json(self.breezy),
            "stenchy": _coords_to_json(self.stenchy),
            "inference_rounds": self.inference_rounds,
        }

    def _apply_inference(self) -> None:
        while True:
            before = self._fact_signature()
            self.inference_rounds += 1

            for square in self.no_breeze:
                for neighbor in self.adjacent(square):
                    self.no_pit.add(neighbor)

            for square in self.no_stench:
                for neighbor in self.adjacent(square):
                    self.no_wumpus.add(neighbor)

            for pit_square in list(self.known_pits):
                self.no_wumpus.add(pit_square)

            if self.known_wumpus is not None:
                self.no_pit.add(self.known_wumpus)
                for square in self.cells():
                    if square != self.known_wumpus:
                        self.no_wumpus.add(square)

            self._infer_pits()
            self._infer_wumpus()

            self.safe = {
                square
                for square in self.cells()
                if square in self.no_pit and square in self.no_wumpus
            }
            self.safe.update(self.visited)
            self.safe.difference_update(self.known_pits)
            if self.known_wumpus is not None:
                self.safe.discard(self.known_wumpus)

            self._refresh_possible_hazards()

            after = self._fact_signature()
            if after == before:
                return

    def _infer_pits(self) -> None:
        for square in self.breezy:
            candidates = {
                neighbor
                for neighbor in self.adjacent(square)
                if neighbor not in self.no_pit
            }
            if len(candidates) == 1:
                pit_square = next(iter(candidates))
                self.known_pits.add(pit_square)
                self.no_wumpus.add(pit_square)

    def _infer_wumpus(self) -> None:
        candidate_sets: list[set[Coord]] = []

        for square in self.stenchy:
            candidates = {
                neighbor
                for neighbor in self.adjacent(square)
                if neighbor not in self.no_wumpus
            }
            if len(candidates) == 1:
                self.known_wumpus = next(iter(candidates))
                self.no_pit.add(self.known_wumpus)
            if candidates:
                candidate_sets.append(candidates)

        if self.known_wumpus is None and candidate_sets:
            intersection = set.intersection(*candidate_sets)
            if len(intersection) == 1:
                wumpus_coord = next(iter(intersection))
                self.known_wumpus = wumpus_coord
                self.no_pit.add(wumpus_coord)

        if self.known_wumpus is not None:
            for square in self.cells():
                if square != self.known_wumpus:
                    self.no_wumpus.add(square)

    def _refresh_possible_hazards(self) -> None:
        possible_pits: set[Coord] = set()
        for square in self.breezy:
            candidates = {
                neighbor
                for neighbor in self.adjacent(square)
                if neighbor not in self.no_pit and neighbor not in self.known_pits
            }
            if len(candidates) > 1:
                possible_pits.update(candidates)

        possible_wumpus: set[Coord] = set()
        if self.known_wumpus is None:
            for square in self.stenchy:
                candidates = {
                    neighbor
                    for neighbor in self.adjacent(square)
                    if neighbor not in self.no_wumpus
                }
                if len(candidates) > 1:
                    possible_wumpus.update(candidates)

        self.possible_pits = possible_pits - self.safe - self.no_pit
        self.possible_wumpus = possible_wumpus - self.safe - self.no_wumpus

    def _fact_signature(self) -> tuple[object, ...]:
        return (
            frozenset(self.visited),
            frozenset(self.safe),
            frozenset(self.breezy),
            frozenset(self.no_breeze),
            frozenset(self.stenchy),
            frozenset(self.no_stench),
            frozenset(self.no_pit),
            frozenset(self.no_wumpus),
            frozenset(self.known_pits),
            self.known_wumpus,
            frozenset(self.possible_pits),
            frozenset(self.possible_wumpus),
        )
