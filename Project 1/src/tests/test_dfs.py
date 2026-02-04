# tests/test_dfs.py
import pytest

from dfs import DFS
from grid import move


# ---------- Helper assertion functions ----------

def assert_metrics_shape(metrics):
    required = {"expanded_states", "generated_nodes", "max_frontier_size", "runtime_ms", "status"}
    assert required.issubset(metrics.keys())

    assert metrics["expanded_states"] >= 0
    assert metrics["generated_nodes"] >= 1
    assert metrics["max_frontier_size"] >= 1
    assert metrics["runtime_ms"] >= 0
    assert metrics["status"] in {"success", "failure"}


def assert_path_starts_ends(states, actions, start, goal, status):
    if status == "success":
        assert states, "Success must return a non-empty path"
        assert states[0] == start, "Path must start at S"
        assert states[-1] == goal, "Path must end at G"
        assert len(actions) == len(states) - 1, "Actions must align with state transitions"
    else:
        assert states == [], "Failure should return empty states"
        assert actions == [], "Failure should return empty actions"


def assert_legal_moves(states, m, n):
    # all states in bounds
    for (r, c) in states:
        assert 0 <= r < m and 0 <= c < n, f"State out of bounds: {(r, c)}"

    # each step is exactly one U/D/L/R move
    for i in range(len(states) - 1):
        (r1, c1) = states[i]
        (r2, c2) = states[i + 1]
        assert abs(r1 - r2) + abs(c1 - c2) == 1, (
            f"Illegal move: {states[i]} -> {states[i+1]} (not U/D/L/R)"
        )


def assert_actions_match(states, actions):
    assert len(actions) == max(0, len(states) - 1), "Actions must align with state transitions"

    for i, a in enumerate(actions):
        assert a in {"U", "D", "L", "R"}, f"Invalid action token: {a}"
        expected_next = move(states[i], a)
        assert expected_next == states[i + 1], (
            f"Action mismatch at step {i}: {states[i]} --{a}--> "
            f"{expected_next}, but path has {states[i+1]}"
        )


# ---------- Tests (expanded like BFS) ----------

def test_dfs_success_path_starts_and_ends():
    m, n = 4, 4
    start = (0, 0)
    goal = (3, 3)

    states, actions, metrics = DFS(start, goal, m, n)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "success"
    assert_path_starts_ends(states, actions, start, goal, "success")


def test_dfs_success_moves_are_legal_and_match_actions():
    m, n = 5, 5
    start = (0, 0)
    goal = (4, 4)

    states, actions, metrics = DFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert_legal_moves(states, m, n)
    assert_actions_match(states, actions)


def test_dfs_failure_out_of_bounds_goal_returns_empty_and_failure():
    """
    Open grid has no walls, so DFS only fails if goal is unreachable.
    Easiest unreachable case: goal outside grid bounds.
    """
    m, n = 3, 3
    start = (0, 0)
    goal = (3, 3)  # out of bounds

    states, actions, metrics = DFS(start, goal, m, n)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "failure"
    assert_path_starts_ends(states, actions, start, goal, "failure")


def test_dfs_start_is_goal():
    m, n = 5, 5
    start = (2, 2)
    goal = (2, 2)

    states, actions, metrics = DFS(start, goal, m, n)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "success"
    assert states == [start]
    assert actions == []


def test_dfs_metrics_present_and_non_negative_on_success():
    m, n = 6, 6
    start = (0, 0)
    goal = (5, 5)

    states, actions, metrics = DFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert_metrics_shape(metrics)


def test_dfs_path_has_no_repeated_states():
    """
    Extracted path should not repeat states (no cycles) even if DFS explores deeply.
    """
    m, n = 6, 6
    start = (0, 0)
    goal = (5, 5)

    states, actions, metrics = DFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert len(states) == len(set(states)), "Solution path repeated a state (cycle)"
