import pytest

from bfs import BFS


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def assert_success(states, actions, metrics, start, goal):
    assert metrics["status"] == "success"

    # endpoints
    assert states[0] == start
    assert states[-1] == goal

    # actions count vs states count
    assert len(actions) == max(0, len(states) - 1)

    # metrics
    assert metrics["generated_nodes"] >= 1
    assert metrics["expanded_states"] >= 0
    assert metrics["max_frontier_size"] >= 1
    assert metrics["runtime_ms"] >= 0


def assert_failure(states, actions, metrics):
    assert metrics["status"] == "failure"
    assert states == []
    assert actions == []
    assert metrics["generated_nodes"] >= 1
    assert metrics["expanded_states"] >= 0
    assert metrics["max_frontier_size"] >= 0
    assert metrics["runtime_ms"] >= 0


def test_bfs():
    # case: 3 3 0 0 2 2 ... bfs
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = BFS(start, goal, m, n)

    assert_success(states, actions, metrics, start, goal)

    # shortest path length should be Manhattan distance
    assert len(actions) == manhattan(start, goal) == 4


def test_bfs_start_equals_goal():
    m, n = 3, 3
    start = goal = (1, 1)

    states, actions, metrics = BFS(start, goal, m, n)

    assert metrics["status"] == "success"
    assert states == [start]
    assert actions == []
    assert metrics["generated_nodes"] == 1
    # In your BFS, goal is checked immediately after pop, before explored-add
    assert metrics["expanded_states"] == 0


@pytest.mark.parametrize(
    "m,n,start,goal,expected_steps",
    [
        (1, 1, (0, 0), (0, 0), 0), # trivial case: start == goal
        (2, 2, (0, 0), (1, 1), 2), # min steps = down, right
        (3, 3, (2, 2), (0, 0), 4), # min steps = up, up, left, left
        (4, 5, (0, 0), (3, 4), 7), # min steps = down x3, right x4
    ],
)

def test_bfs_shortest_path_length_on_empty_grid(m, n, start, goal, expected_steps):
    states, actions, metrics = BFS(start, goal, m, n)

    assert_success(states, actions, metrics, start, goal)
    assert len(actions) == expected_steps
    assert len(actions) == manhattan(start, goal)


def test_bfs_moves_stay_in_bounds():
    m, n = 3, 3
    start = (0, 0)
    goal = (2, 2)

    states, actions, metrics = BFS(start, goal, m, n)
    assert_success(states, actions, metrics, start, goal)

    for (r, c) in states:
        assert 0 <= r < m
        assert 0 <= c < n
