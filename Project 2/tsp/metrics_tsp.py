# tsp/metrics_tsp.py

import json
import math
from collections import defaultdict
from pathlib import Path

RESULTS_FILE = "results/results_tsp.json"
OUT_JSON = "metrics/tsp_metrics_report.json"
OUT_CSV  = "metrics/tsp_metrics_report.csv"

METRICS = ["initial_cost", "best_cost", "iterations", "runtime_ms"]


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def stdev(xs):
    if len(xs) < 2:
        return 0.0 if xs else None
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def safe_num(x):
    return None if x is None else float(x)


def main():
    path = Path(RESULTS_FILE)
    if not path.exists():
        raise FileNotFoundError(f"Missing {RESULTS_FILE}")

    data = json.loads(path.read_text())
    runs = data.get("runs", [])
    if not isinstance(runs, list):
        raise ValueError("results_tsp.json must contain a top-level {'runs': [...]} list")

    # Ensure output dir exists
    Path("metrics").mkdir(parents=True, exist_ok=True)

    # Group by (n_cities, algorithm, operator)  ✅ like A* grouping
    groups = defaultdict(list)
    for r in runs:
        key = (r.get("n_cities"), r.get("algorithm"), r.get("operator"))
        groups[key].append(r)

    report = {"by_group": [], "by_seed": [], "overall": {}, "notes": {}}

    # --------
    # By-group summary (across ALL restart-runs)
    # --------
    for (n_cities, alg, op), rs in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        row = {
            "n_cities": n_cities,
            "algorithm": alg,
            "operator": op,
            "num_runs": len(rs),  # each run is a restart record
        }

        # Standard metrics
        for metric in METRICS:
            vals = []
            for r in rs:
                v = safe_num(r.get(metric))
                if v is not None:
                    vals.append(v)

            row[metric] = {
                "mean": mean(vals),
                "min": min(vals) if vals else None,
                "max": max(vals) if vals else None,
                "stdev": stdev(vals) if vals else None,
            }

        # Improvement achieved = initial_cost - best_cost
        improvements = []
        for r in rs:
            ic = safe_num(r.get("initial_cost"))
            bc = safe_num(r.get("best_cost"))
            if ic is not None and bc is not None:
                improvements.append(ic - bc)

        row["improvement"] = {
            "mean": mean(improvements),
            "min": min(improvements) if improvements else None,
            "max": max(improvements) if improvements else None,
            "stdev": stdev(improvements) if improvements else None,
        }

        report["by_group"].append(row)

    # --------
    # Best tour cost across restarts (per seed) + overall
    # --------
    # For each (n_cities, operator, seed), take min(best_cost) across its restarts.
    per_seed = defaultdict(list)  # key: (n_cities, operator) -> list of best_per_seed
    per_seed_rows = []

    # Group by seed first
    seed_groups = defaultdict(list)
    for r in runs:
        key = (r.get("n_cities"), r.get("operator"), r.get("seed"))
        seed_groups[key].append(r)

    for (n_cities, op, seed), rs in sorted(seed_groups.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        best_costs = [safe_num(r.get("best_cost")) for r in rs if safe_num(r.get("best_cost")) is not None]
        if not best_costs:
            continue
        best_per_seed = min(best_costs)

        per_seed[(n_cities, op)].append(best_per_seed)
        per_seed_rows.append({
            "n_cities": n_cities,
            "operator": op,
            "seed": seed,
            "best_cost_across_restarts": best_per_seed
        })

    report["by_seed"] = per_seed_rows

    # Overall summary per (n_cities, operator)
    overall_rows = []
    for (n_cities, op), bests in sorted(per_seed.items(), key=lambda x: (x[0][0], x[0][1])):
        overall_rows.append({
            "n_cities": n_cities,
            "operator": op,
            "num_seeds": len(bests),
            "best_cost_across_restarts_per_seed": {
                "mean": mean(bests),
                "min": min(bests) if bests else None,
                "max": max(bests) if bests else None,
                "stdev": stdev(bests) if bests else None,
            },
            "overall_best_cost": min(bests) if bests else None,
        })

    report["overall"] = {"by_size_operator": overall_rows}

    report["notes"] = {
        "runs_definition": "Each run in results_tsp.json is ONE restart (one hill-climb to convergence).",
        "grouping": "Grouped by (n_cities, algorithm, operator) for summary stats; per-seed best is computed as min(best_cost) across restarts for each seed.",
        "required_metrics": [
            "initial_cost vs best_cost (improvement)",
            "iterations to converge",
            "best tour cost across restarts (per seed and overall)",
            "runtime_ms",
        ],
    }

    Path(OUT_JSON).write_text(json.dumps(report, indent=2) + "\n")

    # --------
    # CSV output (similar vibe to your A* CSV)
    # --------
    csv_lines = []
    header = [
        "n_cities", "algorithm", "operator", "num_runs",
        "initial_cost_mean", "best_cost_mean", "improvement_mean",
        "iterations_mean", "runtime_ms_mean",
        "overall_best_cost", "best_cost_across_restarts_per_seed_mean"
    ]
    csv_lines.append(",".join(header))

    # Build lookup for overall stats to include on each group row
    overall_lookup = {}
    for row in report["overall"]["by_size_operator"]:
        overall_lookup[(row["n_cities"], row["operator"])] = row

    def fmt(x):
        return "" if x is None else f"{x:.4f}"

    for row in report["by_group"]:
        n_cities = row["n_cities"]
        op = row["operator"]
        overall = overall_lookup.get((n_cities, op), {})

        best_per_seed_mean = None
        if overall:
            best_per_seed_mean = overall["best_cost_across_restarts_per_seed"]["mean"]

        line = [
            str(n_cities),
            str(row["algorithm"]),
            str(op),
            str(row["num_runs"]),
            fmt(row["initial_cost"]["mean"]),
            fmt(row["best_cost"]["mean"]),
            fmt(row["improvement"]["mean"]),
            fmt(row["iterations"]["mean"]),
            fmt(row["runtime_ms"]["mean"]),
            fmt(overall.get("overall_best_cost")),
            fmt(best_per_seed_mean),
        ]
        csv_lines.append(",".join(line))

    Path(OUT_CSV).write_text("\n".join(csv_lines) + "\n")

    print(f"Wrote {OUT_JSON} and {OUT_CSV}")
    print("Tip: open metrics/tsp_metrics_report.csv in Excel and make your TSP tables/plots.")


if __name__ == "__main__":
    main()
