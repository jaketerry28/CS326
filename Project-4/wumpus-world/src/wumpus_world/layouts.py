"""Predefined Wumpus World layouts."""

from __future__ import annotations

from dataclasses import dataclass

Coord = tuple[int, int]


def sort_coords(coords: set[Coord] | frozenset[Coord] | list[Coord]) -> list[Coord]:
    """Return coordinates in a stable row-major order."""
    return sorted(coords, key=lambda coord: (coord[0], coord[1]))


@dataclass(frozen=True, slots=True)
class WumpusLayout:
    """Static definition of a Wumpus World instance."""

    name: str
    size: int
    start: Coord
    pits: frozenset[Coord]
    wumpus: Coord
    description: str

    def cells(self) -> list[Coord]:
        return [(row, col) for row in range(self.size) for col in range(self.size)]


def _layout(
    name: str,
    *,
    size: int,
    start: Coord,
    pits: set[Coord],
    wumpus: Coord,
    description: str,
) -> WumpusLayout:
    if start in pits:
        raise ValueError(f"Layout {name} places a pit on the start square.")
    if start == wumpus:
        raise ValueError(f"Layout {name} places the Wumpus on the start square.")
    if wumpus in pits:
        raise ValueError(f"Layout {name} overlaps the Wumpus and a pit.")

    return WumpusLayout(
        name=name,
        size=size,
        start=start,
        pits=frozenset(pits),
        wumpus=wumpus,
        description=description,
    )


WUMPUS_LAYOUTS: dict[str, WumpusLayout] = {
    "easy_1": _layout(
        "easy_1",
        size=4,
        start=(0, 0),
        pits={(3, 3)},
        wumpus=(3, 0),
        description=(
            "Corner hazards keep the early game simple. "
            "Most safe squares are exposed quickly through no-breeze and no-stench rules."
        ),
    ),
    "easy_2": _layout(
        "easy_2",
        size=4,
        start=(0, 0),
        pits={(1, 3)},
        wumpus=(3, 3),
        description=(
            "Hazards stay on the right side of the board so the agent can safely expand "
            "from the left before resolving the final uncertain squares."
        ),
    ),
    "hard_1": _layout(
        "hard_1",
        size=4,
        start=(0, 0),
        pits={(2, 2)},
        wumpus=(3, 1),
        description=(
            "A central pit and lower-middle Wumpus create overlapping breeze and stench "
            "signals that require additional inference."
        ),
    ),
    "hard_2": _layout(
        "hard_2",
        size=4,
        start=(0, 0),
        pits={(1, 2)},
        wumpus=(2, 1),
        description=(
            "Early overlapping clues appear near the center of the board, so uncertainty "
            "lasts longer before the hazards can be isolated."
        ),
    ),
}


def get_layout(name: str) -> WumpusLayout:
    """Fetch a named layout and raise a readable error when it is missing."""
    try:
        return WUMPUS_LAYOUTS[name]
    except KeyError as exc:
        valid = ", ".join(sorted(WUMPUS_LAYOUTS))
        raise ValueError(f"Unknown Wumpus layout '{name}'. Valid layouts: {valid}.") from exc
