# Analysis of BFS, DFS, and UCS Performance

| m  | n  | algorithm | num_runs | num_success | num_failure | steps_mean | total_cost_mean | expanded_states_mean | max_frontier_size_mean | runtime_ms_mean |
|----|----|-----------|----------|-------------|-------------|------------|-----------------|----------------------|------------------------|-----------------|
| 10 | 10 | bfs       | 10       | 10          | 0           | 18.0000    | 193.9000        | 99.0000              | 37.0000                | 0.3083          |
| 10 | 10 | dfs       | 10       | 10          | 0           | 90.0000    | 952.4000        | 90.0000              | 196.0000               | 0.2654          |
| 10 | 10 | ucs       | 10       | 10          | 0           | 18.2000    | 115.4000        | 98.7000              | 71.7000                | 0.5827          |
| 25 | 25 | bfs       | 10       | 10          | 0           | 48.0000    | 499.8000        | 624.0000             | 97.0000                | 2.7335          |
| 25 | 25 | dfs       | 10       | 10          | 0           | 624.0000   | 6523.0000       | 624.0000             | 1452.0000              | 3.0680          |
| 25 | 25 | ucs       | 10       | 10          | 0           | 49.2000    | 261.9000        | 623.2000             | 214.3000               | 6.0034          |
| 50 | 50 | bfs       | 10       | 10          | 0           | 98.0000    | 1054.2000       | 2499.0000            | 197.0000               | 14.2298         |
| 50 | 50 | dfs       | 10       | 10          | 0           | 2450.0000  | 25670.1000      | 2450.0000            | 5956.0000              | 17.7270         |
| 50 | 50 | ucs       | 10       | 10          | 0           | 100.6000   | 538.0000        | 2497.7000            | 435.7000               | 23.7310         |


## Why BFS Usually Finds a Short Path in Steps but Uses a Lot of Memory

Breadth-First Search (BFS) explores the state space **level by level**, expanding all nodes at depth 1 before depth 2, then depth 3, and so on. Because of this strategy, BFS is **guaranteed to find the shortest path in terms of number of steps** when all actions have equal step cost.

This behavior is reflected in the results:

- On a **10×10 grid**, BFS finds paths averaging **18 steps**
- On a **25×25 grid**, BFS finds paths averaging **48 steps**
- On a **50×50 grid**, BFS finds paths averaging **98 steps**

However, BFS can consume a lot of memory because it must store **every frontier node at the current depth** before moving deeper.

Examples from the data:

- **10x10 BFS**
  - Expanded states mean: **99.0**
  - Max frontier size mean: **37.0**
- **25×25 BFS**
  - Expanded states mean: **624.0**
  - Max frontier size mean: **97.0**
- **50×50 BFS**
  - Expanded states mean: **2499.0**
  - Max frontier size mean: **197.0**

As grid size increases, the frontier can become large, which is why BFS often has high memory usage even when it finds short paths.

---

## Why DFS Is Unpredictable

Depth-First Search (DFS) explores **one branch as deeply as possible** before backtracking. It does not prioritize short paths or low-cost paths, so its performance depends heavily on:

- The order of successors (e.g., U/D/L/R)
- The grid structure
- The random seed

That’s why DFS can sometimes find a solution quickly, but other times it takes a long detour.

The results show DFS taking much longer paths:

- **10×10 DFS**
  - Steps mean: **90.0**
  - Total cost mean: **952.4**
  - Max frontier size mean: **196.0**
- **25×25 DFS**
  - Steps mean: **624.0**
  - Total cost mean: **6523.0**
  - Max frontier size mean: **1452.0**
- **50×50 DFS**
  - Steps mean: **2450.0**
  - Total cost mean: **25670.1**
  - Max frontier size mean: **5956.0**

DFS is therefore unpredictable and not reliable for finding good (short or cheap) paths.

---

## Why UCS Finds a Lower-Cost Path When Costs Vary (Even If It Uses More Steps)

Uniform-Cost Search (UCS) expands the node with the **lowest cumulative cost** first (lowest `g(n)`), not the fewest steps. Because of this, UCS is guaranteed to find the **minimum total cost** path when costs are non-uniform.

The results show that UCS consistently produces lower-cost solutions than BFS:

- **10×10**
  - BFS cost mean: **193.9**
  - UCS cost mean: **115.4**
- **25×25**
  - BFS cost mean: **499.8**
  - UCS cost mean: **261.9**
- **50×50**
  - BFS cost mean: **1054.2**
  - UCS cost mean: **538.0**

This happens because UCS is willing to take “detours” (more steps) to avoid expensive cells, whereas BFS ignores cost and only cares about steps.

UCS often runs slower due to priority queue operations, which is also visible in the runtime means:

- **50×50**
  - BFS runtime mean: **14.2298 ms**
  - UCS runtime mean: **23.7310 ms**

---

## Concrete Example: BFS vs. UCS (50×50 Grid, Seed = 10)

Using a 50×50 grid with randomly generated action costs in the range [1, 20] and random seed = 10:

- **Breadth-First Search (BFS)** found a path with **fewer steps** but a **higher total cost**:
  - Steps: 98  
  - Total cost: 1028  

- **Uniform-Cost Search (UCS)** found a path with **more steps** but a **lower total cost**:
  - Steps: 102  
  - Total cost: 557  

This example clearly shows the tradeoff between the two algorithms. BFS minimizes the number of steps and therefore reaches the goal with a shorter path in terms of distance, but it ignores action costs, resulting in a much higher total cost. In contrast, UCS considers cumulative path cost and is willing to take additional steps to avoid expensive actions, producing a significantly cheaper path overall.


---

## Summary Comparison

| Algorithm | Optimizes | Strength | Weakness |
|----------|----------|----------|----------|
| BFS | Steps | Shortest path in steps | High memory usage (large frontier) |
| DFS | None | Simple implementation | Unpredictable; can take huge detours |
| UCS | Cost | Lowest total path cost | Slower + larger frontier due to PriorityQueue |
