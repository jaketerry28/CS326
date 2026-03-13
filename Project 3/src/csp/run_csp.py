import argparse
import json
import os

from .run_sudoku import run_sudoku
from .run_map import run_map


def save_result(result):
    os.makedirs("results", exist_ok=True)

    filename = f"{result['problem']}_{result['instance']}_{result['config']}.json"
    filename = filename.lower().replace(" ", "_").replace("+", "plus")

    path = os.path.join("results", filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    return path


def print_summary(result):
    print("\n" + "=" * 50)
    print(f"Problem: {result['problem']}")
    print(f"Instance: {result['instance']}")
    print(f"Config: {result['config']}")
    print(f"Solved: {result['solved']}")
    print(f"Runtime ms: {result['runtime_ms']:.3f}")
    print(f"Assignments tried: {result['assignments_tried']}")
    print(f"Backtracks: {result['backtracks']}")
    print("Solution:")

    solution = result["solution"]

    # Sudoku printing
    if result["problem"] == "sudoku":
        for row in solution:
            print(" ".join(map(str, row)))

    # Map coloring printing
    else:
        for region, color in solution.items():
            print(f"{region}: {color}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", required=True, choices=["sudoku", "map"])
    parser.add_argument("--instance", required=True)
    parser.add_argument("--config", required=True)

    args = parser.parse_args()

    if args.problem == "sudoku":
        result = run_sudoku(args.instance, args.config)
    else:
        result = run_map(args.instance, args.config)

    print_summary(result)
    output_path = save_result(result)
    print(f"\nSaved JSON to: {output_path}")


if __name__ == "__main__":
    main()