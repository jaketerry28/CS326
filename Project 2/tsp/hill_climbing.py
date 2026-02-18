# tsp/hill_climbing.py

import time
from tsp.tsp import tour_cost, random_tour, iter_two_opt_moves, two_opt_delta, apply_two_opt


def hill_climb_best_improvement(initial_tour, cities):
    """
    Algorithm 1 Hill Climbing with 2-opt (Best-Improvement)
    Optimized using O(1) 2-opt delta evaluation.
    """
    current = list(initial_tour)
    current_cost = tour_cost(current, cities)
    iterations = 0

    while True:
        best_move = None
        best_delta = 0.0  # best improvement (most negative). 0 means no improvement found.

        for (i, k) in iter_two_opt_moves(current):
            delta = two_opt_delta(current, cities, i, k)
            if delta < best_delta:
                best_delta = delta
                best_move = (i, k)

        if best_move is None:
            return current, current_cost, iterations
        else:
            i, k = best_move
            current = apply_two_opt(current, i, k)
            current_cost = current_cost + best_delta
            iterations += 1



def random_restart_hill_climbing(n_cities, cities, restarts, seed, operator, rng):
    """
    Algorithm 2 Random Restart Hill Climbing
    """

    # 1: bestOverall ← None
    best_overall = None
    best_overall_cost = None

    restart_records = []

    # 2: for i = 1 to N restarts do
    for i in range(1, restarts + 1):

        # 3: current ← random initial tour
        initial = random_tour(n_cities, rng)
        initial_cost = tour_cost(initial, cities)

        start_time = time.perf_counter()

        # 4: localBest ← HillClimbing(current)
        local_best, local_best_cost, iterations = hill_climb_best_improvement(initial, cities)

        runtime_ms = int((time.perf_counter() - start_time) * 1000)

        # JSON record for THIS restart
        restart_records.append({
            "algorithm": "tsp local search",
            "n_cities": n_cities,
            "seed": seed,
            "restarts": restarts,
            "operator": operator,
            "restart_index": i,
            "initial_tour": initial,
            "initial_cost": initial_cost,
            "best_tour": local_best,
            "best_cost": local_best_cost,
            "iterations": iterations,
            "runtime_ms": runtime_ms
        })

        # 5: if bestOverall is None or cost(localBest) < cost(bestOverall) then
        if best_overall is None or local_best_cost < best_overall_cost:
            # 6: bestOverall ← localBest
            best_overall = local_best
            best_overall_cost = local_best_cost

        # 7-8: end if / end for

    # 9: return bestOverall
    return best_overall, best_overall_cost, restart_records

