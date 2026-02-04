# tests/test_ucs.py
import pytest

from ucs import UCS
from grid import move, buildCosts


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
    for (r, c) in states:
        assert 0 <= r < m and 0 <= c < n, f"State out of bounds: {(r, c)}"

    for i in range(len(states) - 1):
        (r1, c1) = states[i]
        (r2, c2) = states[i + 1]
        assert abs(r1 - r2) + abs(c1 - c2) == 1, (
            f"Illegal move: {states[i]} -> {states[i+1]}"
        )


def assert_actions_match(states, actions):
    assert len(actions) == max(0, len(states) - 1), "Actions must align with states"

    for i, a in enumerate(actions):
        assert a in {"U", "D", "L", "R"}, f"Invalid action: {a}"
        expected_next = move(states[i], a)
        assert expected_next == states[i + 1], f"Action mismatch at step {i}"


def recompute_total_cost(states, actions, costs):
    total = 0
    for i, a in enumerate(actions):
        total += costs[(states[i], a)]
    return total


def assert_total_cost_matches(metrics, states, actions, costs):
    assert "total_cost" in metrics, "UCS must report total_cost"
    recomputed = recompute_total_cost(states, actions, costs)
    assert recomputed == metrics["total_cost"], (
        f"Cost mismatch: recomputed={recomputed}, reported={metrics['total_cost']}"
    )


# ---------- Tests (expanded like BFS/DFS) ----------

def test_ucs_success_path_starts_and_ends():
    m, n = 4, 4
    start = (0, 0)
    goal = (3, 3)

    costs = buildCosts(m, n, 1, 5, 42)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "success"
    assert_path_starts_ends(states, actions, start, goal, "success")


def test_ucs_success_moves_are_legal_and_match_actions():
    m, n = 5, 5
    start = (0, 0)
    goal = (4, 4)

    costs = buildCosts(m, n, 1, 9, 7)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert metrics["status"] == "success"
    assert_legal_moves(states, m, n)
    assert_actions_match(states, actions)


def test_ucs_reports_correct_total_cost():
    m, n = 4, 4
    start = (0, 0)
    goal = (3, 3)

    min_cost, max_cost, seed = 1, 5, 42
    costs = buildCosts(m, n, min_cost, max_cost, seed)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert metrics["status"] == "success"
    assert_total_cost_matches(metrics, states, actions, costs)


def test_ucs_failure_out_of_bounds_goal_returns_empty_and_failure():
    m, n = 3, 3
    start = (0, 0)
    goal = (3, 3)  # out of bounds -> unreachable

    costs = buildCosts(m, n, 1, 5, 1)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "failure"
    assert_path_starts_ends(states, actions, start, goal, "failure")


def test_ucs_start_is_goal():
    m, n = 5, 5
    start = (2, 2)
    goal = (2, 2)

    costs = buildCosts(m, n, 1, 5, 123)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert_metrics_shape(metrics)
    assert metrics["status"] == "success"
    assert states == [start]
    assert actions == []
    # cost should be 0 if reported (optional, depends on your UCS implementation)
    if "total_cost" in metrics:
        assert metrics["total_cost"] == 0


def test_ucs_metrics_present_and_non_negative_on_success():
    m, n = 6, 6
    start = (0, 0)
    goal = (5, 5)

    costs = buildCosts(m, n, 1, 10, 99)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert metrics["status"] == "success"
    assert_metrics_shape(metrics)


def test_ucs_path_has_no_repeated_states():
    m, n = 6, 6
    start = (0, 0)
    goal = (5, 5)

    costs = buildCosts(m, n, 1, 10, 5)

    states, actions, metrics = UCS(start, goal, m, n, costs)

    assert metrics["status"] == "success"
    assert len(states) == len(set(states)), "Solution path repeated a state (cycle)"
