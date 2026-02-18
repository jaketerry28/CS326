## A* Experimental Comparison and Discussion

### A* Metrics Table
| m  | n  | algorithm | heuristic | num_runs | num_success | num_failure | steps_mean | total_cost_mean | expanded_states_mean | max_frontier_size_mean | runtime_ms_mean |
|----|----|-----------|-----------:|----------|-------------|-------------|------------|-----------------|----------------------|------------------------|-----------------|
| 10 | 10 | astar     | euclidean |       10 |          10 |           0 |    18.4000 |         56.6000 |             304.0000 |                78.8000 |          0.4016 |
| 10 | 10 | astar     | manhattan |       10 |          10 |           0 |    18.2000 |         56.6000 |             298.3000 |                85.6000 |          0.4154 |
| 25 | 25 | astar     | euclidean |       10 |          10 |           0 |    48.2000 |        134.3000 |            2355.6000 |               246.3000 |          3.2609 |
| 25 | 25 | astar     | manhattan |       10 |          10 |           0 |    48.2000 |        134.3000 |            2351.4000 |               291.0000 |          3.1621 |
| 50 | 50 | astar     | euclidean |       10 |          10 |           0 |    99.4000 |        264.7000 |            9730.1000 |               529.6000 |         13.4580 |
| 50 | 50 | astar     | manhattan |       10 |          10 |           0 |    99.4000 |        264.7000 |            9720.3000 |               642.7000 |         11.9480 |

*Runtime_ms_mean is the only metric that should change after running experiments and metrics analysis.*

## A* Search (Grid World)

### 1. Steps (Path Length)

Across all grid sizes (10×10, 25×25, 50×50), the returned path lengths scale linearly with grid dimension.  

The expected shortest path from (0,0) to (m−1,n−1) in a grid without obstacles is:


```(m - 1) + (n - 1)```

Observed averages:
- 10×10 → ≈ 18 steps
- 25×25 → ≈ 48 steps
- 50×50 → ≈ 99 steps

These closely match theoretical shortest Manhattan distance values, confirming that A* is returning optimal paths when using admissible heuristics.

---

### 2. Total Cost

Total path cost increases proportionally with grid size. Because edge costs are randomly generated in the range [1, 9], the optimal path avoids high-cost edges whenever possible.

Both Manhattan and Euclidean heuristics return identical total costs, which confirms:
- Both heuristics are admissible.
- A* finds optimal solutions regardless of which admissible heuristic is used.

The differences between heuristics appear only in efficiency metrics, not solution quality.

---

### 3. Expanded States

The number of expanded states grows rapidly with grid size:
- ~300 (10×10)
- ~2,300 (25×25)
- ~9,700 (50×50)

Manhattan consistently expands slightly fewer states than Euclidean. This is expected because Manhattan distance more accurately reflects actual shortest-path cost in 4-directional grid movement.

This demonstrates the key benefit of informed search:
- A better heuristic reduces state expansion.
- A* focuses search toward the goal instead of expanding uniformly outward like UCS.

---

### 4. Max Frontier Size

The maximum frontier size also increases with grid size. Larger grids produce wider wavefronts of exploration.

Manhattan generally produces a somewhat larger frontier than Euclidean in some cases, due to differences in expansion shape and tie-breaking. However, both remain significantly more efficient than uninformed search would be.

---

### 5. Runtime

Runtime scales with grid size:
- ~0.4 ms (10×10)
- ~3 ms (25×25)
- ~12 ms (50×50)

This growth aligns with the increase in expanded states. Since A* explores thousands of nodes for larger grids, runtime is roughly proportional to expansion count.

Overall, A* demonstrates strong scalability for moderately sized grids.

---

### TSP Metrics Table

| n_cities | algorithm | operator | num_runs | initial_cost_mean | best_cost_mean | improvement_mean | iterations_mean | runtime_ms_mean | overall_best_cost | best_cost_across_restarts_per_seed_mean |
|----------|-----------|----------|----------|-------------------|----------------|------------------|-----------------|-----------------|-------------------|----------------------------------------|
| 20 | tsp local search | two_opt | 100 | 1105.3343 | 406.1232 | 699.2110 | 14.9800 | 1.8500 | 362.2844 | 396.0458 |
| 30 | tsp local search | two_opt | 100 | 1601.0416 | 493.0356 | 1108.0060 | 24.0700 | 7.9500 | 437.5190 | 475.2905 |
| 50 | tsp local search | two_opt | 100 | 2606.9082 | 618.3194 | 1988.5887 | 44.7900 | 43.1900 | 559.7490 | 596.4401 |

## TSP Local Search (2-Opt)

### 1. Initial Cost vs Best Cost

Across all problem sizes, the average initial tour cost is significantly higher than the final best cost found after applying 2-opt local search.

Observed averages:

- 20 cities  
  - Initial ≈ 1105.33  
  - Best ≈ 406.12  
  - Improvement ≈ 699.21  

- 30 cities  
  - Initial ≈ 1601.04  
  - Best ≈ 493.04  
  - Improvement ≈ 1108.01  

- 50 cities  
  - Initial ≈ 2606.91  
  - Best ≈ 618.32  
  - Improvement ≈ 1988.59  

This demonstrates that 2-opt is highly effective at improving randomly generated tours. As the number of cities increases, the absolute improvement becomes larger because:

- Random tours become increasingly inefficient.
- There are more crossing edges that 2-opt can eliminate.
- The search space grows combinatorially, offering more opportunities for improvement.

However, improvement does not guarantee global optimality, since 2-opt only explores neighboring solutions.

---

### 2. Solution Quality (Best Cost)

The average best tour cost increases with the number of cities:

- 20 cities → ≈ 406  
- 30 cities → ≈ 493  
- 50 cities → ≈ 618  

While total cost increases, it grows much slower than the initial random tour cost. This indicates:

- 2-opt consistently finds high-quality local optima.
- Local search scales reasonably in terms of solution quality.

The **overall best cost** across all runs is always lower than the average best cost, showing that multiple restarts can lead to better solutions.

---

### 3. Iterations to Convergence

Average number of improvement iterations:

- 20 cities → ≈ 15 iterations  
- 30 cities → ≈ 24 iterations  
- 50 cities → ≈ 45 iterations  

This shows that convergence speed decreases as problem size increases. Larger instances require more local improvements before reaching a local minimum.

Even so, convergence remains relatively fast compared to the enormous size of the TSP search space (which is factorial in n).

---

### 4. Runtime

Runtime scales significantly with the number of cities:

- 20 cities → ≈ 1.85 ms  
- 30 cities → ≈ 7.95 ms  
- 50 cities → ≈ 43.19 ms  

Runtime increases faster than linearly due to:

- More possible 2-opt swaps (O(n²) neighborhood size).
- More iterations required to reach convergence.

Despite this, runtime remains small even for 50 cities, highlighting the efficiency of local search compared to exact search methods.

---

### 5. Effect of Restarts

The metric `best_cost_across_restarts_per_seed_mean` shows that performing multiple random restarts improves solution quality beyond a single run.

Additionally, the presence of an `overall_best_cost` lower than the mean best cost confirms:

- Different runs converge to different local minima.
- TSP local search is highly sensitive to initialization.
- Restart strategies are essential for improving solution robustness.

---

### Overall Interpretation

2-opt local search:

- Dramatically improves random tours.
- Converges quickly relative to the exponential search space.
- Scales reasonably in runtime for moderate n.
- Remains susceptible to local minima, requiring restarts for better results.

This confirms the expected behavior of local search for NP-hard problems like TSP:
efficient, scalable, and practical — but not guaranteed to find the global optimum.


# Conceptual Analysis

## Why A* Expands Fewer States Than UCS

Uniform-Cost Search (UCS) expands nodes in increasing order of g(n) only, without considering proximity to the goal.

A* expands nodes in increasing order of:


```f(n) = g(n) + h(n)```


If h(n) is admissible (never overestimates the true cost), then:

- A* preserves optimality.
- A* biases exploration toward the goal.
- Many nodes UCS would explore are never considered by A*.

Thus, A* reduces unnecessary expansions by incorporating heuristic guidance.

---

## Why A* Is Still Exponential in the Worst Case

Even with a heuristic, the search space grows exponentially in branching factor and depth.

If:
- The heuristic provides little guidance (e.g., very weak heuristic),
- Or many paths have similar f-values,
- Or costs vary unpredictably,

then A* may still explore a very large portion of the state space.

Formally, in the worst case A* can still expand O(b^d) nodes, where:
- b = branching factor
- d = solution depth

The heuristic improves average-case performance but does not eliminate exponential worst-case complexity.

---

## Why Exact Search Is Infeasible for TSP

The number of possible tours in TSP grows factorially:

(n − 1)! / 2

This growth is extremely fast. Even for 20 cities, the number of possible tours is astronomically large. Exact algorithms (like brute force or full search) require exponential or factorial time, making them impractical for moderate n. Therefore, approximate methods are necessary.

---

## Why Local Search Converges Quickly

Local search begins with a complete solution and repeatedly applies small improvements (e.g., 2-opt swaps). Each step strictly improves cost until no better neighbor exists.

Because:
- Each move reduces cost,
- The neighborhood is efficiently searchable (O(n²) for 2-opt),
- Many crossings can be removed early,

the algorithm rapidly improves poor initial tours and reaches a local minimum in relatively few iterations.

---

## Why Local Search Can Get Stuck in Local Minima

Local search only explores neighboring solutions. Once no improving move exists, it stops — even if a better global solution exists elsewhere.

This happens because:
- The search is greedy.
- It does not explore worse intermediate states.
- The landscape contains many local optima.

Thus, different initial tours may converge to different final solutions.

---

## Effect of Neighborhood Operator

The neighborhood operator determines which solutions are reachable from the current state.

For 2-opt:
- Removes two edges and reconnects the tour.
- Eliminates crossings efficiently.
- Balances solution quality and computational cost.

Stronger operators (e.g., 3-opt) explore larger neighborhoods and may find better solutions but increase runtime.

---

### Concrete Example: Same n (20), Different Local Minima

Algorithm: tsp local search  
Operator: two_opt  
Restarts: 10  
Coord range: (0.0, 100.0)  

## Run A — Seed = 42

Restart 1:  initial=1180.879  best=353.553  iters=17  runtime_ms=2  
Restart 2:  initial=1046.191  best=352.318  iters=17  runtime_ms=2  
Restart 3:  initial=942.242   best=353.553  iters=13  runtime_ms=2  
Restart 4:  initial=981.959   best=352.318  iters=16  runtime_ms=2  
Restart 5:  initial=1017.003  best=352.318  iters=14  runtime_ms=2  
Restart 6:  initial=1212.760  best=352.318  iters=17  runtime_ms=2  
Restart 7:  initial=984.068   best=352.318  iters=14  runtime_ms=2  
Restart 8:  initial=1044.884  best=352.318  iters=17  runtime_ms=2  
Restart 9:  initial=1054.750  best=352.318  iters=18  runtime_ms=2  
Restart 10: initial=1106.740  best=352.318  iters=13  runtime_ms=2  

Best overall cost: **352.318**  
Best overall tour:  
[12, 19, 14, 18, 10, 15, 2, 7, 16, 17, 8, 5, 6, 13, 1, 11, 4, 0, 9, 3]

Observation: Most restarts converge to the same local minimum (352.318), with a few slightly worse plateaus (353.553).

## Run B — Seed = 43

Restart 1:  initial=1065.967  best=394.139  iters=15  runtime_ms=2  
Restart 2:  initial=941.292   best=400.823  iters=14  runtime_ms=2  
Restart 3:  initial=986.403   best=419.546  iters=15  runtime_ms=2  
Restart 4:  initial=1086.355  best=392.198  iters=15  runtime_ms=2  
Restart 5:  initial=1004.345  best=392.198  iters=11  runtime_ms=2  
Restart 6:  initial=1109.210  best=383.370  iters=16  runtime_ms=2  
Restart 7:  initial=1147.561  best=393.508  iters=16  runtime_ms=2  
Restart 8:  initial=1035.798  best=386.124  iters=17  runtime_ms=2  
Restart 9:  initial=1018.944  best=392.198  iters=17  runtime_ms=2  
Restart 10: initial=1088.344  best=394.139  iters=12  runtime_ms=1  

Best overall cost: **383.370**  
Best overall tour:  
[14, 5, 18, 6, 2, 8, 11, 16, 15, 19, 13, 9, 7, 10, 12, 3, 1, 4, 0, 17]

Observation: The best solution here (383.370) is significantly worse than the best from Seed 42 (352.318), even with identical algorithm settings.


**What this demonstrates**
- Both runs use the same neighborhood operator (2-opt) and restart strategy, yet they converge to *different* locally optimal tours.
- Because 2-opt only accepts improving swaps, once a tour has no improving 2-opt move, it becomes “stuck” in that local minimum.
- Different random city layouts (different seeds) produce different cost landscapes, so the local minima reached (and their quality) can differ substantially.


---

# Overall Conclusion

- A* efficiently finds optimal paths using admissible heuristics and expands far fewer states than UCS.
- However, A* remains exponential in the worst case.
- TSP exact search is infeasible due to factorial growth.
- Local search (2-opt) scales well and quickly improves solutions.
- It does not guarantee global optimality and may converge to different local minima.
- Restart strategies improve robustness.

These results highlight the tradeoff between exact optimal methods and scalable heuristic approaches in AI.

