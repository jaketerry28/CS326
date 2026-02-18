import json
import sys
import random
from pathlib import Path

from astar.grid import buildCosts
from astar.a_star import astar
from astar.heuristic import manhattan, euclidean

from tsp.tsp import generate_cities
from tsp.hill_climbing import random_restart_hill_climbing

RESULTS_FILE = "results.json"


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


def path_cost(states, actions, costs):
    total = 0
    for i in range(len(actions)):
        total += costs[(states[i], actions[i])]
    return total


def main():
    args = sys.argv[1:]

    # Mode selection
    # A*:  python main.py astar m n rs cs rg cg min_cost max_cost seed heuristic
    # TSP: python main.py tsp n_cities coord_min coord_max restarts seed operator
    if len(args) == 0:
        mode = input("Mode (astar/tsp): ").strip().lower()
    else:
        mode = args[0].strip().lower()

    # -------------------------
    # A* MODE
    # -------------------------
    if mode == "astar":
        a = args[1:]  # after mode

        # Accept CLI args or interactive input
        if len(a) == 10:
            m, n, rs, cs, rg, cg, min_cost, max_cost, seed = map(int, a[:9])
            heuristic_name = a[9].lower()
        elif len(args) == 0:
            m = int(input("Enter number of rows (m): "))
            n = int(input("Enter number of columns (n): "))
            rs = int(input(f"Enter start row (0-{m-1}): "))
            cs = int(input(f"Enter start column (0-{n-1}): "))
            rg = int(input(f"Enter goal row (0-{m-1}): "))
            cg = int(input(f"Enter goal column (0-{n-1}): "))
            min_cost = int(input("Enter minimum cost: "))
            max_cost = int(input("Enter maximum cost: "))
            seed = int(input("Enter random seed: "))
            heuristic_name = input("Heuristic (manhattan/euclidean): ").strip().lower()
        else:
            print("Usage: python main.py astar m n rs cs rg cg min_cost max_cost seed heuristic")
            return

        # Pick heuristic function
        if heuristic_name == "manhattan":
            heuristic_fn = manhattan
        elif heuristic_name == "euclidean":
            heuristic_fn = euclidean
        else:
            print("Error: heuristic must be 'manhattan' or 'euclidean'")
            return

        start = (rs, cs)
        goal = (rg, cg)

        # Validation
        if m <= 0 or n <= 0:
            print("Error: grid size must be positive.")
            return

        if min_cost > max_cost:
            print("Error: min_cost must be <= max_cost.")
            return

        if not (0 <= start[0] < m and 0 <= start[1] < n):
            print("Error: start state is outside the grid.")
            return

        if not (0 <= goal[0] < m and 0 <= goal[1] < n):
            print("Error: goal state is outside the grid.")
            return

        # Build reproducible directed edge costs
        costs = buildCosts(m, n, min_cost, max_cost, seed)

        # Run A*
        result = astar(m, n, start, goal, costs, heuristic_fn=heuristic_fn)

        # Print terminal output
        print("Algorithm: astar")
        print("Grid:", f"{m}x{n}")
        print("Start:", start)
        print("Goal:", goal)
        print("Cost range:", (min_cost, max_cost))
        print("Seed:", seed)
        print("Heuristic:", heuristic_name)
        print("Status:", result["status"])

        if result["status"] == "success":
            print("Steps:", result["steps"])
            print("Total cost:", result["total_cost"])
            print("Expanded states:", result["expanded_states"])
            print("Generated nodes:", result["generated_nodes"])
            print("Max frontier size:", result["max_frontier_size"])
            print("Runtime (ms):", round(result["runtime_ms"], 3))
            print("Path states:", result["states"])
            print("Path actions:", result["actions"])

            # Sanity check: recompute cost from path
            recomputed = path_cost(result["states"], result["actions"], costs)
            if recomputed != result["total_cost"]:
                print("ERROR: Path cost mismatch!")
                print("Recomputed:", recomputed)
                print("Reported:", result["total_cost"])
        else:
            print("Status: failure (no path found)")

        # Save JSON output (required fields)
        run_record = {
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

        append_result(run_record, RESULTS_FILE)

    # -------------------------
    # TSP MODE
    # -------------------------
    elif mode == "tsp":
        a = args[1:]  # after mode

        # python main.py tsp n_cities coord_min coord_max restarts seed operator
        if len(a) == 6:
            n_cities = int(a[0])
            coord_min = float(a[1])
            coord_max = float(a[2])
            restarts = int(a[3])
            seed = int(a[4])
            operator = a[5].strip().lower()
        elif len(args) == 0:
            n_cities = int(input("Enter number of cities (n): "))
            coord_min = float(input("Enter coord min (e.g., 0): "))
            coord_max = float(input("Enter coord max (e.g., 100): "))
            restarts = int(input("Enter number of restarts: "))
            seed = int(input("Enter random seed: "))
            operator = input("Operator (two_opt): ").strip().lower()
        else:
            print("Usage: python main.py tsp n_cities coord_min coord_max restarts seed operator")
            return

        # Validation
        if n_cities <= 1:
            print("Error: n_cities must be >= 2.")
            return

        if coord_min > coord_max:
            print("Error: coord_min must be <= coord_max.")
            return

        if restarts <= 0:
            print("Error: restarts must be positive.")
            return

        if operator != "two_opt":
            print("Error: operator must be 'two_opt'")
            return

        # Reproducible RNG for BOTH cities + initial tours
        rng = random.Random(seed)

        cities = generate_cities(n_cities, rng, coord_min=coord_min, coord_max=coord_max)

        best_tour, best_cost, restart_records = random_restart_hill_climbing(
            n_cities=n_cities,
            cities=cities,
            restarts=restarts,
            seed=seed,
            operator=operator,
            rng=rng
        )

        # Print terminal output (required)
        print("Algorithm: tsp local search")
        print("n_cities:", n_cities)
        print("Coord range:", (coord_min, coord_max))
        print("Seed:", seed)
        print("Restarts:", restarts)
        print("Operator:", operator)

        for r in restart_records:
            print(
                f"Restart {r['restart_index']}: "
                f"initial={round(r['initial_cost'], 3)} "
                f"best={round(r['best_cost'], 3)} "
                f"iters={r['iterations']} "
                f"runtime_ms={r['runtime_ms']}"
            )

            # Save ONE JSON record per restart (your chosen structure)
            append_result(r, RESULTS_FILE)

        print("Best overall cost:", round(best_cost, 3))
        print("Best overall tour:", best_tour)

    else:
        print("Error: mode must be 'astar' or 'tsp'")
        print("A*:  python main.py astar m n rs cs rg cg min_cost max_cost seed heuristic")
        print("TSP: python main.py tsp n_cities coord_min coord_max restarts seed operator")
        return


if __name__ == "__main__":
    main()
