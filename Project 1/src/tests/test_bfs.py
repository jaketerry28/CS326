# tests/test_bfs.py
import pytest

from bfs import BFS
from grid import move


# ---------- Helper assertions ----------

def assert_metrics_shape(metrics):
    """Metrics must exist and be non-negative."""
    required = {"expanded_states", "generated_nodes", "max_frontier_size", "runtime_ms", "status"}
    assert required.issubset(metrics.keys())

    assert metrics["expanded_states"] >= 0
    assert metrics["generated_nodes"] >= 1
    assert metrics["max_frontier_size"] >= 1
    assert metrics["runtime_ms"] >= 0
    assert metrics["status"] in {"success", "failure"}


def assert_path_starts_ends(states, actions, start, goal, status):
    """Path and actions must be consistent with status."""
    if status == "success":
        assert states, "Success must return a non-empty states path"
        assert states[0] == start, "Path must start at s0"
        assert states[-1] == goal, "Path must end at goal"
        assert len(actions) == len(states) - 1, "actions must be one less than states"
    else:
        assert states == [], "Failure must return empty states"
        assert actions == [], "Failure must return empty actions"


def assert_all_states_in_bounds(states, m, n):
    for (r, c) in states:
        assert 0 <= r < m and 0 <= c < n, f"Out of bounds state: {(r, c)}"


def assert_actions_match_moves(states, actions):
    """Each action should transform states[i] -> states[i+1] via grid.move."""
    for i, a in enumerate(actions):
        expected = move(states[i], a)
        assert expected == states[i + 1], f"Action {a} did not match move from {states[i]} to {states[i+1]}"


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def assert_consecutive_are_adjacent(states):
    """Each consecutive pair must differ by exactly 1 step (U/D/L/R)."""
    for i in range(len(states) - 1):
        assert manhattan(states[i], states[i + 1]) == 1, f"Non-adjacent step: {states[i]} -> {states[i+1]}"


# ---------- Tests you were missing ----------

def test_bfs_success_path_starts_and_ends():
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = BFS(start, goal, m, n)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "success"
    assert_path_starts_ends(states, actions, start, goal, "success")


def test_bfs_success_moves_are_legal_and_match_actions():
    m, n = 4, 4
    start = (0, 0)
    goal = (3, 3)

    states, actions, metrics = BFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert_all_states_in_bounds(states, m, n)
    assert_consecutive_are_adjacent(states)
    assert_actions_match_moves(states, actions)


def test_bfs_returns_shortest_steps_on_uniform_grid():
    """
    On an open 3x3 grid with 4-neighborhood moves,
    shortest path from (0,0) to (2,2) is 4 steps.
    BFS must return that shortest length.
    """
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = BFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert len(actions) == 4
    assert len(states) == 5


def test_bfs_failure_out_of_bounds_goal_returns_empty_and_failure():
    """
    Your BFS will fail if the goal is unreachable.
    Since your grid has no walls, the easiest unreachable case is a goal
    outside the grid (it will never be generated).
    """
    m, n = 3, 3
    start = (0, 0)
    goal = (3, 3)  # out of bounds

    states, actions, metrics = BFS(start, goal, m, n)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "failure"
    assert_path_starts_ends(states, actions, start, goal, "failure")


def test_bfs_start_is_goal():
    m, n = 5, 5
    start = (2, 2)
    goal = (2, 2)

    states, actions, metrics = BFS(start, goal, m, n)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "success"
    assert states == [start]
    assert actions == []


def test_bfs_path_has_no_repeated_states():
    """
    Extracted solution path should not repeat states.
    (Even though your BFS may generate duplicates in the frontier,
     the final extracted path should be a simple path.)
    """
    m, n = 6, 6
    start = (0, 0)
    goal = (5, 5)

    states, actions, metrics = BFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert len(states) == len(set(states)), "Solution path repeated a state (cycle)"
