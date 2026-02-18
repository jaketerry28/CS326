import json
import time
from pathlib import Path

from .grid import buildCosts
from .a_star import astar
from .heuristic import manhattan, euclidean

RESULTS_FILE = "results/results_astar.json"


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

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def run_one(m, n, start, goal, min_cost, max_cost, seed, heuristic_name, heuristic_fn):
    costs = buildCosts(m, n, min_cost, max_cost, seed)
    result = astar(m, n, start, goal, costs, heuristic_fn=heuristic_fn)

    return {
        "algorithm": "astar",
        "m": m,
        "n": n,
        "start": list(start),
        "goal": list(goal),
        "min_cost": min_cost,
        "max_cost": max_cost,
        "seed": seed,
        "heuristic": heuristic_name,
        "path": [list(s) for s in result["states"]],
        "steps": result["steps"],
        "total_cost": result["total_cost"],
        "expanded_states": result["expanded_states"],
        "generated_nodes": result["generated_nodes"],
        "max_frontier_size": result["max_frontier_size"],
        "runtime_ms": result["runtime_ms"],
        "status": result["status"],
    }


def main():
    # Required grid sizes
    grid_sizes = [(10, 10), (25, 25), (50, 50)]

    # Choose 10 seeds (you can change these, but keep them fixed for reproducibility)
    seeds = [1, 2, 3, 4, 5, 10, 20, 30, 50, 100]

    # Cost range (use your project defaults; change if you want)
    min_cost = 1
    max_cost = 9

    # Start/goal (pick something consistent; corners are standard)
    start = (0, 0)

    heuristics = [
        ("manhattan", manhattan),
        ("euclidean", euclidean),  # optional (you implemented it)
    ]

    total_runs = 0
    t0 = time.perf_counter()

    for (m, n) in grid_sizes:
        goal = (m - 1, n - 1)

        for seed in seeds:
            for heuristic_name, heuristic_fn in heuristics:
                record = run_one(
                    m=m,
                    n=n,
                    start=start,
                    goal=goal,
                    min_cost=min_cost,
                    max_cost=max_cost,
                    seed=seed,
                    heuristic_name=heuristic_name,
                    heuristic_fn=heuristic_fn,
                )
                append_result(record, RESULTS_FILE)
                total_runs += 1

                print(
                    f"[{total_runs:02d}] {m}x{n} seed={seed} h={heuristic_name} "
                    f"status={record['status']} steps={record['steps']} "
                    f"cost={record['total_cost']} expanded={record['expanded_states']} "
                    f"frontier_max={record['max_frontier_size']} runtime_ms={record['runtime_ms']:.3f}"
                )

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    print(f"\nDone. Wrote {total_runs} runs to {RESULTS_FILE}. Total runtime: {elapsed_ms:.2f} ms")


if __name__ == "__main__":
    main()
