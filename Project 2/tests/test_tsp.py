import random

from tsp.tsp import (
    generate_cities,
    random_tour,
    tour_cost,
    iter_two_opt_moves,
    two_opt_delta,
)

from tsp.hill_climbing import hill_climb_best_improvement


def test_tour_is_valid_permutation_each_city_once():
    n = 30
    rng = random.Random(123)
    tour = random_tour(n, rng)

    assert len(tour) == n
    assert sorted(tour) == list(range(n))  # each city appears exactly once


def test_tour_cost_is_closed_cycle_returns_to_start():
    # 2-city case is the simplest proof:
    # cycle cost must include 0->1 and 1->0, so it equals 2 * dist(0,1)
    cities = [(0.0, 0.0), (3.0, 4.0)]  # distance = 5
    tour = [0, 1]

    cost = tour_cost(tour, cities)

    assert cost == 10.0  # 5 + 5 (must return to start)


def test_hill_climbing_terminates_no_improving_neighbor_exists():
    n = 20
    seed = 7
    rng = random.Random(seed)
    cities = generate_cities(n, rng, coord_min=0, coord_max=100)

    start_tour = random_tour(n, rng)
    final_tour, final_cost, iterations = hill_climb_best_improvement(start_tour, cities)

    # sanity: it should converge in finite steps
    assert iterations >= 0

    # termination condition: no improving 2-opt move exists
    # i.e., for all moves, delta >= 0
    for (i, k) in iter_two_opt_moves(final_tour):
        assert two_opt_delta(final_tour, cities, i, k) >= 0.0
