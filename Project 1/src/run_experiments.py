import json
from pathlib import Path

from grid import buildCosts
from main import run_bfs, run_dfs, run_ucs


def main():
    cfg = json.loads(Path("experiment_config.json").read_text())

    results_file = cfg.get("results_file", "results.json")
    min_cost = int(cfg["min_cost"])
    max_cost = int(cfg["max_cost"])

    start = tuple(cfg["start"])
    sizes = cfg["sizes"]
    seeds = cfg["seeds"]
    algorithms = [a.lower() for a in cfg["algorithms"]]

    total_runs = 0

    for m, n in sizes:
        m, n = int(m), int(n)

        #Goal changes with grid size (bottom-right)
        goal = (m - 1, n - 1)

        for seed in seeds:
            seed = int(seed)
            costs = buildCosts(m, n, min_cost, max_cost, seed)

            for alg in algorithms:
                if alg == "bfs":
                    run_bfs(start, goal, m, n, costs, min_cost, max_cost, seed)
                elif alg == "dfs":
                    run_dfs(start, goal, m, n, costs, min_cost, max_cost, seed)
                elif alg == "ucs":
                    run_ucs(start, goal, m, n, costs, min_cost, max_cost, seed)
                else:
                    raise ValueError(f"Unknown algorithm: {alg}")

                total_runs += 1

    print(f"Done. Total runs: {total_runs} (expected 90)")
    print(f"Results appended to: {results_file}")


if __name__ == "__main__":
    main()
