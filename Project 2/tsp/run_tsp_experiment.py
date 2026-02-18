# tsp/run_tsp_experiment.py

import json
import time
import random
from pathlib import Path

from .tsp import generate_cities
from .hill_climbing import random_restart_hill_climbing

RESULTS_FILE = "results/results_tsp.json"


def append_result(result, filename=RESULTS_FILE):
    path = Path(filename)

    if path.exists():
        try:
            with open(path, "r") as f:
                data = json.load(f)
            if "runs" not in data or not isinstance(data["runs"], list):
                data = {"runs": []}
        except (json.JSONDecodeError, OSError):
            data = {"runs": []}
    else:
        data = {"runs": []}

    data["runs"].append(result)

    # Ensure output folder exists
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def run_one(n_cities, coord_min, coord_max, restarts, seed, operator):
    """
    Runs ONE seed worth of TSP work, producing ONE JSON record per restart
    (so 10 restarts == 10 runs in the JSON log).
    """
    rng = random.Random(seed)

    cities = generate_cities(
        n=n_cities,
        rng=rng,
        coord_min=coord_min,
        coord_max=coord_max
    )

    best_tour, best_cost, restart_records = random_restart_hill_climbing(
        n_cities=n_cities,
        cities=cities,
        restarts=restarts,
        seed=seed,
        operator=operator,
        rng=rng
    )

    return best_tour, best_cost, restart_records


def main():
    # Required problem sizes
    problem_sizes = [20, 30, 50]

    # Choose 10 seeds (keep fixed for reproducibility)
    seeds = [1, 2, 3, 4, 5, 10, 20, 30, 50, 100]

    # Coordinate range (project example)
    coord_min = 0
    coord_max = 100

    # Required restarts per seed
    restarts = 10

    # Chosen operator (must match your implementation)
    operator = "two_opt"

    total_runs = 0
    t0 = time.perf_counter()

    for n_cities in problem_sizes:
        for seed in seeds:
            best_tour, best_cost, restart_records = run_one(
                n_cities=n_cities,
                coord_min=coord_min,
                coord_max=coord_max,
                restarts=restarts,
                seed=seed,
                operator=operator
            )

            # Each restart counts as one run in the logs
            for r in restart_records:
                append_result(r, RESULTS_FILE)
                total_runs += 1

                print(
                    f"[{total_runs:03d}] n={n_cities} seed={seed} "
                    f"restart={r['restart_index']:02d}/{restarts} op={operator} "
                    f"init={r['initial_cost']:.3f} best={r['best_cost']:.3f} "
                    f"iters={r['iterations']} runtime_ms={r['runtime_ms']}"
                )

            # Optional per-seed summary line (keeps output readable)
            print(f"  -> seed summary: n={n_cities} seed={seed} best_overall={best_cost:.3f}")

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    print(f"\nDone. Wrote {total_runs} runs to {RESULTS_FILE}. Total runtime: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()
