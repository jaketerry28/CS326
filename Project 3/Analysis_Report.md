# Analysis Report

## Table of Results

| Problem | Instance   | Config     | Solved | Runtime (ms) | Assignments Tried | Backtracks |
|---------|------------|------------|--------|--------------|-------------------|------------|
| map     | australia  | baseline   | True   | 0.06         | 7                 | 0          |
| map     | australia  | mrv        | True   | 0.08         | 7                 | 0          |
| map     | australia  | mrv fc     | True   | 0.08         | 7                 | 0          |
| map     | australia  | mrv fc lcv | True   | 0.09         | 7                 | 0          |
| sudoku  | easy_1     | baseline   | True   | 17.64        | 61                | 27         |
| sudoku  | easy_1     | mrv        | True   | 56.08        | 2410              | 2376       |
| sudoku  | easy_1     | mrv fc     | True   | 18.23        | 44                | 7          |
| sudoku  | easy_1     | mrv fc lcv | True   | 18.92        | 48                | 10         |
| sudoku  | easy_2     | baseline   | True   | 39.56        | 2999              | 2954       |
| sudoku  | easy_2     | mrv        | True   | 260.94       | 16865             | 16820      |
| sudoku  | easy_2     | mrv fc     | True   | 17.21        | 51                | 5          |
| sudoku  | easy_2     | mrv fc lcv | True   | 18.49        | 51                | 5          |
| sudoku  | medium_1   | baseline   | True   | 28.06        | 1469              | 1420       |
| sudoku  | medium_1   | mrv        | True   | 3959.59      | 257224            | 257175     |
| sudoku  | medium_1   | mrv fc     | True   | 17.66        | 83                | 30         |
| sudoku  | medium_1   | mrv fc lcv | True   | 19.43        | 116               | 60         |
| sudoku  | medium_2   | baseline   | True   | 20.40        | 701               | 654        |
| sudoku  | medium_2   | mrv        | True   | 432.15       | 23336             | 23289      |
| sudoku  | medium_2   | mrv fc     | True   | 17.09        | 132               | 78         |
| sudoku  | medium_2   | mrv fc lcv | True   | 16.46        | 81                | 32         |
| sudoku  | hard_1     | baseline   | True   | 41.32        | 3360              | 3310       |
| sudoku  | hard_1     | mrv        | True   | 3317.34      | 171500            | 171450     |
| sudoku  | hard_1     | mrv fc     | True   | 19.90        | 206               | 149        |
| sudoku  | hard_1     | mrv fc lcv | True   | 16.74        | 50                | 0          |
| sudoku  | hard_2     | baseline   | True   | 41.65        | 3360              | 3310       |
| sudoku  | hard_2     | mrv        | True   | 3331.97      | 171500            | 171450     |
| sudoku  | hard_2     | mrv fc     | True   | 20.24        | 206               | 149        |
| sudoku  | hard_2     | mrv fc lcv | True   | 16.92        | 50                | 0          |
| sudoku  | extreme_1  | baseline   | True   | 769.09       | 87316             | 87261      |
| sudoku  | extreme_1  | mrv        | True   | 4674.01      | 270769            | 270714     |
| sudoku  | extreme_1  | mrv fc     | True   | 17.81        | 140               | 78         |
| sudoku  | extreme_1  | mrv fc lcv | True   | 26.83        | 447               | 358        |

---

## Effect of MRV on the Search Tree

The Minimum Remaining Values (MRV) heuristic selects the variable with the smallest domain, aiming to expose conflicts early. However, MRV alone can increase assignments and backtracks, especially in Sudoku. For example, in the medium_1 Sudoku instance:

| Configuration | Assignments Tried | Backtracks |
|---------------|------------------|------------|
| Baseline      | 1469             | 1420       |
| MRV           | 257224           | 257175     |

MRV changes variable ordering but does not remove inconsistent domain values, sometimes guiding the search toward difficult parts without preventing invalid combinations. When combined with forward checking (FC), MRV becomes more effective:

| Configuration | Assignments Tried | Backtracks |
|---------------|------------------|------------|
| MRV + FC      | 83               | 30         |

MRV works best when paired with constraint propagation techniques that actively prune the search space.

---

## Effect of Forward Checking

Forward checking prunes domains after each assignment, detecting failures early. For example, in the easy_2 Sudoku instance:

| Configuration | Assignments Tried | Backtracks |
|---------------|------------------|------------|
| Baseline      | 2999             | 2954       |
| MRV           | 16865            | 16820      |
| MRV + FC      | 51               | 5          |

Forward checking dramatically reduces assignments and backtracks by removing inconsistent values from neighbor domains immediately after each assignment, preventing the solver from exploring large portions of the search tree that would eventually fail.

---

## Differences Between Sudoku and Map Coloring

Sudoku and map coloring differ significantly in constraint structure. Map coloring (e.g., Australia) has a sparse constraint graph, where each region interacts with few neighbors. The solver finds a solution immediately, requiring only 7 assignments and 0 backtracks across all configurations.

Sudoku has a highly connected constraint structure. Each cell is constrained by its row, column, and 3×3 block, resulting in roughly 20 neighboring variables. This dense network increases the likelihood of conflicts and creates a much larger search space. Sudoku benefits much more from heuristics and domain pruning techniques such as MRV and forward checking.

---

## Example of a Domain Wipe-Out Event

A domain wipe-out occurs when constraint propagation removes all possible values from a variable’s domain. When this happens, the solver immediately knows the current branch cannot lead to a valid solution and must backtrack.

During the easy_2 Sudoku run using MRV + Forward Checking, the solver reported:

> Assigning (8, 0) = 6 caused neighbor (5, 0)'s domain to become empty.

After assigning 6 to cell (8, 0), forward checking updated the domains of all neighboring cells. One neighbor, cell (5, 0), had its domain reduced to empty, meaning no legal value remained.

This situation is called a domain wipe-out. The solver immediately stops exploring that branch and backtracks to try a different assignment. This highlights why forward checking is effective: it detects failures immediately, reducing unnecessary search and improving efficiency.

