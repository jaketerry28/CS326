# tsp/tsp.py

import math


def generate_cities(n, rng, coord_min=0, coord_max=100):
    cities = []
    for _ in range(n):
        x = rng.uniform(coord_min, coord_max)
        y = rng.uniform(coord_min, coord_max)
        cities.append((x, y))
    return cities


def random_tour(n, rng):
    tour = list(range(n))
    rng.shuffle(tour)
    return tour


def euclidean(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def tour_cost(tour, cities):
    total = 0
    n = len(tour)

    for i in range(n - 1):
        total += euclidean(cities[tour[i]], cities[tour[i + 1]])

    total += euclidean(cities[tour[-1]], cities[tour[0]])
    return total

def two_opt_delta(tour, cities, i, k):
    """
    O(1) change in tour cost if we reverse tour[i:k+1] (2-opt).
    Returns: (new_cost - old_cost). Negative means improvement.
    """
    n = len(tour)

    a = tour[i - 1]
    b = tour[i]
    c = tour[k]
    d = tour[(k + 1) % n]

    before = euclidean(cities[a], cities[b]) + euclidean(cities[c], cities[d])
    after  = euclidean(cities[a], cities[c]) + euclidean(cities[b], cities[d])

    return after - before


def iter_two_opt_moves(tour):
    """
    Generate (i, k) pairs for 2-opt moves.
    i starts at 1 so i-1 is valid and we avoid special-casing the wrap edge.
    """
    n = len(tour)
    for i in range(1, n - 1):
        for k in range(i + 1, n):
            yield i, k


def apply_two_opt(tour, i, k):
    """
    Apply 2-opt by reversing segment [i:k] and return a NEW tour.
    """
    return tour[:i] + list(reversed(tour[i:k+1])) + tour[k+1:]