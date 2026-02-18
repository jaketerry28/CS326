# tests/test_astar.py
# Run: python -m pytest -q


import pytest

from astar.grid import buildCosts, move, in_bounds, ACTIONS
from astar.a_star import astar
from astar.heuristic import manhattan, euclidean



@pytest.mark.parametrize(
    "heuristic_fn",
    [manhattan, euclidean],
    ids=["manhattan", "euclidean"]
)
def test_path_starts_at_S_and_ends_at_G(heuristic_fn):
    m, n = 10, 10
    start = (0, 0)
    goal = (9, 9)
    min_cost, max_cost, seed = 1, 9, 123

    costs = buildCosts(m, n, min_cost, max_cost, seed)
    result = astar(m, n, start, goal, costs, heuristic_fn=heuristic_fn)

    assert result["status"] == "success"
    assert result["states"][0] == start
    assert result["states"][-1] == goal


@pytest.mark.parametrize(
    "heuristic_fn",
    [manhattan, euclidean],
    ids=["manhattan", "euclidean"]
)
def test_every_move_is_legal_and_stays_in_bounds(heuristic_fn):
    m, n = 10, 10
    start = (0, 0)
    goal = (9, 9)
    min_cost, max_cost, seed = 1, 9, 123

    costs = buildCosts(m, n, min_cost, max_cost, seed)
    result = astar(m, n, start, goal, costs, heuristic_fn=heuristic_fn)

    assert result["status"] == "success"

    states = result["states"]
    actions = result["actions"]

    # Exactly one action per transition
    assert len(actions) == len(states) - 1

    for i, a in enumerate(actions):
        # One of the 4 actions
        assert a in ACTIONS

        s = states[i]
        s_next = move(s, a)

        # Must match the returned next state
        assert s_next == states[i + 1]

        # Must remain in bounds
        assert in_bounds(s_next, m, n)

        # Must exist in cost map (legal move)
        assert (s, a) in costs


@pytest.mark.parametrize(
    "heuristic_fn",
    [manhattan, euclidean],
    ids=["manhattan", "euclidean"]
)
def test_recomputed_total_cost_matches_reported_total_cost(heuristic_fn):
    m, n = 10, 10
    start = (0, 0)
    goal = (9, 9)
    min_cost, max_cost, seed = 1, 9, 123

    costs = buildCosts(m, n, min_cost, max_cost, seed)
    result = astar(m, n, start, goal, costs, heuristic_fn=heuristic_fn)

    assert result["status"] == "success"

    states = result["states"]
    actions = result["actions"]

    recomputed = 0
    for i, a in enumerate(actions):
        recomputed += costs[(states[i], a)]

    assert recomputed == result["total_cost"]
