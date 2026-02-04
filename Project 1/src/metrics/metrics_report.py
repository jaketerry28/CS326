import json
import math
from collections import defaultdict
from pathlib import Path

RESULTS_FILE = "results.json"
OUT_JSON = "metrics/metrics_report.json"
OUT_CSV = "metrics/metrics_report.csv"

METRICS = ["steps", "total_cost", "expanded_states", "max_frontier_size", "runtime_ms"]


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def stdev(xs):
    if len(xs) < 2:
        return 0.0 if xs else None
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def safe_num(x):
    # Convert None to None; int/float pass through
    return None if x is None else float(x)


def main():
    path = Path(RESULTS_FILE)
    if not path.exists():
        raise FileNotFoundError(f"Missing {RESULTS_FILE}")

    data = json.loads(path.read_text())
    runs = data.get("runs", [])
    if not isinstance(runs, list):
        raise ValueError("results.json must contain a top-level {'runs': [...]} list")

    # Group by (m,n,algorithm)
    groups = defaultdict(list)
    for r in runs:
        key = (r.get("m"), r.get("n"), r.get("algorithm"))
        groups[key].append(r)

    report = {"by_group": [], "notes": {}}

    # Build summary rows
    for (m, n, alg), rs in sorted(groups.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        # Optional: only include successes in averages (common in reports)
        successes = [r for r in rs if r.get("status") == "success"]
        failures = [r for r in rs if r.get("status") != "success"]

        row = {
            "m": m,
            "n": n,
            "algorithm": alg,
            "num_runs": len(rs),
            "num_success": len(successes),
            "num_failure": len(failures),
        }

        # For each metric, compute stats over successful runs only
        for metric in METRICS:
            vals = []
            for r in successes:
                v = r.get(metric)
                v = safe_num(v)
                if v is not None:
                    vals.append(v)

            row[metric] = {
                "mean": mean(vals),
                "min": min(vals) if vals else None,
                "max": max(vals) if vals else None,
                "stdev": stdev(vals) if vals else None,
            }

        report["by_group"].append(row)

    # Notes to help you explain choices in the report
    report["notes"] = {
        "aggregation": "Stats computed over successful runs only. Success/failure counts are included per group.",
        "metrics": METRICS,
    }

    Path(OUT_JSON).write_text(json.dumps(report, indent=2) + "\n")

    # Also write a flat CSV table (easy to paste into Word/Google Docs)
    # Columns: m,n,algorithm,num_success + metric_mean columns
    csv_lines = []
    header = ["m", "n", "algorithm", "num_runs", "num_success", "num_failure"] + [f"{m}_mean" for m in METRICS]
    csv_lines.append(",".join(header))

    for row in report["by_group"]:
        line = [
            str(row["m"]),
            str(row["n"]),
            row["algorithm"],
            str(row["num_runs"]),
            str(row["num_success"]),
            str(row["num_failure"]),
        ]
        for metric in METRICS:
            mu = row[metric]["mean"]
            line.append("" if mu is None else f"{mu:.4f}")
        csv_lines.append(",".join(line))

    Path(OUT_CSV).write_text("\n".join(csv_lines) + "\n")

    print(f"Wrote {OUT_JSON} and {OUT_CSV}")
    print("Tip: open metrics_report.csv in Excel and make your comparison tables/plots.")


if __name__ == "__main__":
    main()
