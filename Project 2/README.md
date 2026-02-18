# How To Run Everything (From Project Root)

## 1️⃣ Run Unit Tests

Run all tests:

If pytest has import issues:
```bash
python -m pytest -q
```

PART A — A* SEARCH
---

## 2️⃣ Run A* Experiments (30 grids × heuristics)

This will:
- Run 10×10, 25×25, 50×50
- Use 10 seeds each
- Run Manhattan (required)
- Run Euclidean (optional)
- Append results to results/results_astar.json

```bash
python -m astar.run_astar_experiments
```

⚠️ WARNING:
If `results/results_astar.json` already exists, this will append onto it.

---

## 3️⃣ Generate A* Metrics Report

This reads `results/results_astar.json` and writes:
- metrics/astar_metrics_report.json
- metrics/astar_metrics_report.csv

```bash
python -m astar.metrics_astar
```

Open the CSV in Excel/Sheets for tables & plots.

⚠️ WARNING:
`results/results_astar.json` must already exist.

---

## 4️⃣ Run A* Manually (Single Grid)

Format:
```bash
python main.py astar m n rs cs rg cg min_cost max_cost seed heuristic
```

Example:
```bash
python main.py astar 10 10 0 0 9 9 1 9 123 manhattan
```

or

```bash
python main.py astar 10 10 0 0 9 9 1 9 123 euclidean
```

⚠️ WARNING:
Stores results in separate `results.json` or will append if `results.json` already exists.


---
PART B — TSP LOCAL SEARCH
---

## 5️⃣ Run TSP Experiments (Required 300 Runs)

This will:
- Use 20, 30, 50 cities
- Use 10 seeds per size
- Use 10 random restarts per seed
- Produce 300 restart runs total
- Append results to results/results_tsp.json

```bash
python -m tsp.run_tsp_experiment
```

⚠️ WARNING:
If `results/results_tsp.json` already exists, results will be appended.

---

## 6️⃣ Generate TSP Metrics Report

This reads `results/results_tsp.json` and writes:
- metrics/tsp_metrics_report.json
- metrics/tsp_metrics_report.csv

```bash
python -m tsp.metrics_tsp
```

Open the CSV in Excel/Sheets for analysis and plots.

⚠️ WARNING:
`results/results_tsp.json` must already exist.

---

## 7️⃣ Run TSP Manually (Single Configuration)

Format:
```bash
python main.py tsp n_cities coord_min coord_max restarts seed operator
```

Example:
```bash
python main.py tsp 20 0 100 10 42 two_opt
```

This will:
- Print each restart’s results
- Append each restart as one run to results.json

⚠️ WARNING:
Appending occurs if `results.json` already exists.



---
COMPLETE EXPERIMENT PIPELINE (START → FINISH)
---

1. Delete old results if starting fresh:
   - results/results_astar.json
   - results/results_tsp.json

2. Run:
   - python -m astar.run_astar_experiments
   - python -m tsp.run_tsp_experiment

3. Generate reports:
   - python -m astar.metrics_astar
   - python -m tsp.metrics_tsp

4. Open both CSV files in Excel/Sheets and build tables/plots for your report.

5. Run main for specific test cases. Seeds guarentee reproducability.