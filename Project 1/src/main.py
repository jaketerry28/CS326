import json
import sys
from pathlib import Path
from grid import buildCosts
from dfs import DFS
from bfs import BFS
from ucs import UCS

RESULTS_FILE = "results.json"

def append_result(result, filename="results.json"):
    path = Path(filename)

    if path.exists():
        with open(path, "r") as f:
            try:
                data = json.load(f)
                if "runs" not in data or not isinstance(data["runs"], list):
                    # migrate old format safely
                    data = {"runs": []}
            except json.JSONDecodeError:
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

def run_bfs(start, goal, m, n, costs, min_cost, max_cost, seed):
    # Run BFS

    states, actions, metrics = BFS(start, goal, m, n)    
    total = path_cost(states, actions, costs) if metrics["status"] == "success" else 0


    result = {
        "algorithm": "bfs",
        "m": m,
        "n": n,
        "start": list(start),
        "goal": list(goal),
        "min_cost": min_cost,
        "max_cost": max_cost,
        "seed": seed,
        "path": [list(s) for s in states],
        "steps": len(actions),  # exclude initial None action
        "total_cost": total if metrics["status"] == "success" else None,
        "expanded_states": metrics["expanded_states"],
        "generated_nodes": metrics["generated_nodes"],
        "max_frontier_size": metrics["max_frontier_size"],
        "runtime_ms": metrics["runtime_ms"],
        "status": metrics["status"],
    }

    print(result)


    # Save to file
    append_result(result)


## make like run_bfs for other algorithms

def run_dfs(start, goal, m, n, costs, min_cost, max_cost, seed):
    # Run DFS

    states, actions, metrics = DFS(start, goal, m, n)    
    total = path_cost(states, actions, costs) if metrics["status"] == "success" else 0


    result = {
        "algorithm": "dfs",
        "m": m,
        "n": n,
        "start": list(start),
        "goal": list(goal),
        "min_cost": min_cost,
        "max_cost": max_cost,
        "seed": seed,
        "path": [list(s) for s in states],
        "steps": len(actions),  # exclude initial None action
        "total_cost": total if metrics["status"] == "success" else None,
        "expanded_states": metrics["expanded_states"],
        "generated_nodes": metrics["generated_nodes"],
        "max_frontier_size": metrics["max_frontier_size"],
        "runtime_ms": metrics["runtime_ms"],
        "status": metrics["status"],
    }

    print(result)

    # Save to file
    append_result(result)
    

def run_ucs(start, goal, m, n, costs, min_cost, max_cost, seed):
    # Run UCS

    states, actions, metrics = UCS(start, goal, m, n, costs)    
    total = path_cost(states, actions, costs) if metrics["status"] == "success" else 0


    result = {
        "algorithm": "ucs",
        "m": m,
        "n": n,
        "start": list(start),
        "goal": list(goal),
        "min_cost": min_cost,
        "max_cost": max_cost,
        "seed": seed,
        "path": [list(s) for s in states],
        "steps": len(actions),  # exclude initial None action
        "total_cost": total if metrics["status"] == "success" else None,
        "expanded_states": metrics["expanded_states"],
        "generated_nodes": metrics["generated_nodes"],
        "max_frontier_size": metrics["max_frontier_size"],
        "runtime_ms": metrics["runtime_ms"],
        "status": metrics["status"],
    }

    print(result)

    # Save to file
    append_result(result)



def main():
    args = sys.argv[1:]

    if args:
        if len(args) != 10:
            print("Usage: python main.py m n rs cs rg cg min_cost max_cost seed algorithm")
            return
    
        m, n, rs, cs, rg, cg, min_cost, max_cost, seed = map(int, args[:9])
        algorithm = args[9].lower()

    else:
        # Get user inputs
        m = int(input("Enter number of rows (m): "))
        n = int(input("Enter number of columns (n): "))

        rs = int(input("Enter start row (0-{}): ".format(m-1)))
        cs = int(input("Enter start column (0-{}): ".format(n-1)))
        
        rg = int(input("Enter goal row (0-{}): ".format(m-1)))
        cg = int(input("Enter goal column (0-{}): ".format(n-1)))
        
        min_cost = int(input("Enter minimum cost: "))
        max_cost = int(input("Enter maximum cost: "))
    
        seed = int(input("Enter random seed: "))

        algorithm = input("Enter algorithm (bfs, dfs, ucs): ").lower()

    start = (rs, cs)
    goal = (rg, cg)

    if m <= 0 or n <= 0:
        print("Error: grid size must be positive.")
        return

    if min_cost > max_cost:
        print("Error: min_cost must be <= max_cost.")
        return
    
    if not (0 <= goal[0] < m and 0 <= goal[1] < n):
        print("Error: goal state is outside the grid.")
        return

    if not (0 <= start[0] < m and 0 <= start[1] < n):
        print("Error: start state is outside the grid.")
        return
    
    costs = buildCosts(m, n, min_cost, max_cost, seed)

    if algorithm == "bfs":
        run_bfs(start, goal, m, n, costs, min_cost, max_cost, seed)
    elif algorithm == "dfs":
        run_dfs(start, goal, m, n, costs, min_cost, max_cost, seed)
    elif algorithm == "ucs":
        run_ucs(start, goal, m, n, costs, min_cost, max_cost, seed)
    else:
        print("Error: algorithm must be bfs, dfs, or ucs")
        return



    # # Run BFS
    # run_bfs(start, goal, m, n, costs, min_cost, max_cost, seed)

    # # Run DFS
    # run_dfs(start, goal, m, n, costs, min_cost, max_cost, seed)



if __name__ == "__main__":
    main()