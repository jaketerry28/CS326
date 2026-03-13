import argparse
import json
import os
import csv

from .run_sudoku import run_sudoku
from .run_map import run_map


def save_result(result):
    os.makedirs("results", exist_ok=True)

    json_path = os.path.join("results", "results.json")
    csv_path = os.path.join("results", "results.csv")

    # -----------------------
    # JSON LOG (append style)
    # -----------------------
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(result)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # -----------------------
    # CSV LOG
    # -----------------------
    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # write header once
        if not file_exists:
            writer.writerow([
                "problem",
                "instance",
                "config",
                "solved",
                "runtime_ms",
                "assignments_tried",
                "backtracks"
            ])

        writer.writerow([
            result["problem"],
            result["instance"],
            result["config"],
            result["solved"],
            result["runtime_ms"],
            result["assignments_tried"],
            result["backtracks"]
        ])

    return json_path


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