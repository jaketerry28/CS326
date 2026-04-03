"""Knowledge-based Wumpus World agent."""

from __future__ import annotations

from collections import deque

from .environment import Percept, WumpusWorld
from .knowledge_base import WumpusKnowledgeBase
from .layouts import Coord


def _coord_to_json(coord: Coord | None) -> list[int] | None:
    return None if coord is None else [coord[0], coord[1]]


class KnowledgeBasedWumpusAgent:
    """Agent that only moves into squares the KB has proved safe."""

    def __init__(self, world: WumpusWorld) -> None:
        self.world = world
        self.kb = WumpusKnowledgeBase(size=world.size, start=world.start)
        self.position = world.start

        self.moves_taken = 0
        self.states_expanded = 0
        self.trace: list[dict[str, object]] = []
        self.failed = False
        self.failure_reason: str | None = None

    def run(self) -> dict[str, object]:
        self._observe(action="start", previous=None)

        while not self.failed:
            path = self._nearest_safe_path()
            if path is None:
                break

            for next_square in path[1:]:
                if next_square in self.kb.known_unsafe:
                    self.failed = True
                    self.failure_reason = (
                        f"Refused to move into known unsafe square {next_square}."
                    )
                    break

                previous = self.position
                self.position = next_square
                self.moves_taken += 1

                if self.world.is_hazard(next_square):
                    self.failed = True
                    self.failure_reason = f"Entered a hazard at {next_square}."

                self._observe(action="move", previous=previous)

                if self.failed:
                    break

        actual_safe = self.world.safe_cells()
        fully_explored = self.kb.visited == actual_safe
        success = not self.failed and fully_explored

        if self.failure_reason is None and not success:
            self.failure_reason = (
                "No additional squares could be proved safe, so exploration stopped."
            )

        return {
            "success": success,
            "states_expanded": self.states_expanded,
            "moves_taken": self.moves_taken,
            "trace": self.trace,
            "visited_squares": len(self.kb.visited),
            "total_safe_squares": len(actual_safe),
            "fully_explored": fully_explored,
            "failure_reason": self.failure_reason,
            "knowledge_summary": self.kb.fact_summary(),
        }

    def _observe(self, action: str, previous: Coord | None) -> None:
        first_visit = self.position not in self.kb.visited
        percept = self.world.perceive(self.position)
        self.kb.tell_percept(self.position, percept)
        if first_visit:
            self.states_expanded += 1

        self.trace.append(
            {
                "step": len(self.trace),
                "action": action,
                "from": _coord_to_json(previous),
                "to": _coord_to_json(self.position),
                "percept": percept.to_dict(),
                "adjacent_statuses": self.kb.adjacent_statuses(self.position),
                "knowledge": self.kb.fact_summary(),
            }
        )

    def _nearest_safe_path(self) -> list[Coord] | None:
        allowed = set(self.kb.safe)
        allowed.add(self.position)

        queue: deque[tuple[Coord, list[Coord]]] = deque([(self.position, [self.position])])
        seen = {self.position}

        while queue:
            current, path = queue.popleft()
            if current in self.kb.frontier_safe():
                return path

            for neighbor in self.world.adjacent(current):
                if neighbor in seen or neighbor not in allowed:
                    continue
                seen.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        return None
