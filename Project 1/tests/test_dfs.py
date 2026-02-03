import pytest
from dfs import DFS
from grid import move


def assert_success(states, actions, metrics, start, goal):
    assert metrics["status"] == "success"
    assert states[0] == start
    assert states[-1] == goal
    assert len(actions) == max(0, len(states) - 1)

    assert metrics["generated_nodes"] >= 1
    assert metrics["expanded_states"] >= 0
    assert metrics["max_frontier_size"] >= 1
    assert metrics["runtime_ms"] >= 0


def test_dfs():
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = DFS(start, goal, m, n)
    assert_success(states, actions, metrics, start, goal)


def test_dfs_actions_match_states():
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = DFS(start, goal, m, n)
    assert_success(states, actions, metrics, start, goal)

    # Strong correctness check: each action transitions to the next state
    for i, a in enumerate(actions):
        assert move(states[i], a) == states[i + 1]


def test_dfs_path_stays_in_bounds():
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = DFS(start, goal, m, n)
    assert_success(states, actions, metrics, start, goal)

    for (r, c) in states:
        assert 0 <= r < m
        assert 0 <= c < n


def test_dfs_start_equals_goal():
    m, n = 3, 3
    start = goal = (1, 1)

    states, actions, metrics = DFS(start, goal, m, n)
    assert metrics["status"] == "success"
    assert states == [start]
    assert actions == []

def test_dfs_failure():
    m, n = 2, 2
    start = (0, 0)
    goal = (3, 3)  # outside grid

    states, actions, metrics = DFS(start, goal, m, n)
    assert metrics["status"] == "failure"
    assert states == []
    assert actions == []