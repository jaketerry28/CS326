# Generic CSP Solver Framework

**How to Run the Code**

To run the code, navigate to `../src` and use the following command in the terminal, replacing `<problem>`, `<instance>`, and `<config>` with the appropriate values for the problem you want to solve:


## Map Coloring

```
python -m csp.run_csp --problem map --instance australia --config baseline
python -m csp.run_csp --problem map --instance australia --config mrv
python -m csp.run_csp --problem map --instance australia --config "mrv fc"
python -m csp.run_csp --problem map --instance australia --config "mrv fc lcv"
```

## Sudoku

Sudoku puzzles are provided in the `sudoku_instances` directory. You can run the solver on any of these puzzles using the following command:

- easy_1
```
python -m csp.run_csp --problem sudoku --instance easy_1 --config baseline
python -m csp.run_csp --problem sudoku --instance easy_1 --config mrv
python -m csp.run_csp --problem sudoku --instance easy_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance easy_1 --config "mrv fc lcv"
```
- easy_2
```
python -m csp.run_csp --problem sudoku --instance easy_2 --config baseline
python -m csp.run_csp --problem sudoku --instance easy_2 --config mrv
python -m csp.run_csp --problem sudoku --instance easy_2 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance easy_2 --config "mrv fc lcv"
```
- medium_1
```
python -m csp.run_csp --problem sudoku --instance medium_1 --config baseline
python -m csp.run_csp --problem sudoku --instance medium_1 --config mrv
python -m csp.run_csp --problem sudoku --instance medium_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance medium_1 --config "mrv fc lcv"
```
- medium_2
```
python -m csp.run_csp --problem sudoku --instance medium_2 --config baseline
python -m csp.run_csp --problem sudoku --instance medium_2 --config mrv
python -m csp.run_csp --problem sudoku --instance medium_2 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance medium_2 --config "mrv fc lcv"
```
- hard_1
```
python -m csp.run_csp --problem sudoku --instance hard_1 --config baseline
python -m csp.run_csp --problem sudoku --instance hard_1 --config mrv
python -m csp.run_csp --problem sudoku --instance hard_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance hard_1 --config "mrv fc lcv"
```
- hard_2
```
python -m csp.run_csp --problem sudoku --instance hard_2 --config baseline
python -m csp.run_csp --problem sudoku --instance hard_2 --config mrv
python -m csp.run_csp --problem sudoku --instance hard_2 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance hard_2 --config "mrv fc lcv"
```
- extreme_1 (just for fun, almost worst case scenario)
```
python -m csp.run_csp --problem sudoku --instance extreme_1 --config baseline
python -m csp.run_csp --problem sudoku --instance extreme_1 --config mrv
python -m csp.run_csp --problem sudoku --instance extreme_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance extreme_1 --config "mrv fc lcv"
```

*One line copy-paste commands for all runs:*
```
python -m csp.run_csp --problem map --instance australia --config baseline
python -m csp.run_csp --problem map --instance australia --config mrv
python -m csp.run_csp --problem map --instance australia --config "mrv fc"
python -m csp.run_csp --problem map --instance australia --config "mrv fc lcv"
python -m csp.run_csp --problem sudoku --instance easy_1 --config baseline
python -m csp.run_csp --problem sudoku --instance easy_1 --config mrv
python -m csp.run_csp --problem sudoku --instance easy_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance easy_1 --config "mrv fc lcv"
python -m csp.run_csp --problem sudoku --instance easy_2 --config baseline
python -m csp.run_csp --problem sudoku --instance easy_2 --config mrv
python -m csp.run_csp --problem sudoku --instance easy_2 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance easy_2 --config "mrv fc lcv"
python -m csp.run_csp --problem sudoku --instance medium_1 --config baseline
python -m csp.run_csp --problem sudoku --instance medium_1 --config mrv
python -m csp.run_csp --problem sudoku --instance medium_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance medium_1 --config "mrv fc lcv"
python -m csp.run_csp --problem sudoku --instance medium_2 --config baseline
python -m csp.run_csp --problem sudoku --instance medium_2 --config mrv
python -m csp.run_csp --problem sudoku --instance medium_2 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance medium_2 --config "mrv fc lcv"
python -m csp.run_csp --problem sudoku --instance hard_1 --config baseline
python -m csp.run_csp --problem sudoku --instance hard_1 --config mrv
python -m csp.run_csp --problem sudoku --instance hard_1 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance hard_1 --config "mrv fc lcv"
python -m csp.run_csp --problem sudoku --instance hard_2 --config baseline
python -m csp.run_csp --problem sudoku --instance hard_2 --config mrv
python -m csp.run_csp --problem sudoku --instance hard_2 --config "mrv fc"
python -m csp.run_csp --problem sudoku --instance hard_2 --config "mrv fc lcv"
```

## Run Tests

The project includes unit tests for the generic CSP engine as well as validation tests
for the Sudoku and Map Coloring problem instances.

**Generic CSP engine**
- Constraint checking (`is_consistent`)
- Assignment completion detection (`is_complete`)
- Variable selection heuristics (MRV + Degree tie-break)
- Value ordering heuristic (LCV)
- Forward checking domain pruning
- Arc consistency (`AC-3`)
- Backtracking search
- Solver correctness (`solve()`)

**Sudoku**
- The solver returns a solution when the puzzle is solvable
- The returned grid is **complete** (no empty cells)
- Each **row contains digits 1–9 with no repetition**
- Each **column contains digits 1–9 with no repetition**
- Each **3×3 block contains digits 1–9 with no repetition**

**Map Coloring**
- The solver assigns a **color to every region**
- For every edge `(u, v)` in the map, **color(u) ≠ color(v)**

### Running the tests

Run all tests using:

```
python -m pytest -q
```

# Generic CSP Solver Framework

## Overview

This project implements a **generic Constraint Satisfaction Problem (CSP) solver** that can be reused across multiple problem types. The key design goal is separation of concerns:

* the **solver engine** is generic and problem-independent,
* each **problem instance** defines its own variables, domains, neighbors, and constraint logic,
* runner scripts assemble a problem instance and pass it into the shared CSP engine

Because of that separation, the same backtracking engine can solve both:

1. **Sudoku**, where each grid cell is a variable and constraints enforce no repeated values in rows, columns, or boxes.
2. **Map Coloring**, where each region is a variable and constraints enforce different colors for adjacent regions.


---

## High-Level Architecture

The project is organized into four conceptual layers:

### 1. Generic solver layer

This layer contains the reusable CSP engine.

* `generic_csp.py`

It knows how to:

* represent a CSP,
* test consistency,
* choose variables and values,
* prune domains,
* apply arc consistency,
* run recursive backtracking search.

It does **not** know anything specific about Sudoku or map coloring.

### 2. Problem-definition layer

This layer describes individual CSPs using the same interface expected by the solver.

* `sudoku_instance.py`
* `map_coloring_instance.py`

Each file defines:

* variables,
* initial domains,
* neighbor relationships,
* a constraint function.


### 3. Input-data layer

This layer contains actual problem instances to solve.

* `sudoku_puzzles.py`

For Sudoku, the structural rules stay the same, but each puzzle board is different. This file stores multiple boards grouped by difficulty.

Map coloring does not have multiple instances in this project, but if you wanted to add more maps, you could create a similar data file for that.

### 4. Execution layer

This layer wires everything together and runs experiments.

* `run_sudoku.py`
* `run_map.py`
* `run_csp.py`

These files build a configured `CSP` object, call `solve()`, validate the result, and print the output.

---

## Core Design Principle

The entire project depends on one shared abstraction:

A CSP can be represented by:

* a set of **variables**,
* a **domain** for each variable,
* a **neighbor graph** showing which variables interact,
* a **constraint function** that decides whether two assignments are compatible.

Once a problem is converted into that structure, the same solving logic can be reused.

That is why Sudoku and map coloring can both run through the same engine even though they look like completely different problems.

---

## File-by-File System Design

## `generic_csp.py`

This is the heart of the system. It defines the `CSP` class and contains all search logic.

### Responsibilities

The `CSP` class stores:

* `variables`: all decision variables in the problem,
* `domains`: current legal values for each variable,
* `neighbors`: adjacency/constraint graph,
* `constraint`: a function that evaluates pairwise consistency.

It also stores configuration flags that turn heuristics on or off:

* `use_mrv`
* `use_forward_checking`
* `use_lcv`
* `use_ac3`

It tracks basic search metrics too:

* `assignments_tried`
* `backtracks`

### Major methods

#### `is_consistent(var, value, assignment)`

Checks whether assigning a candidate value to a variable would violate constraints with already-assigned neighbors.

This is the local validity test used before the solver commits to an assignment.

#### `is_complete(assignment)`

Returns `True` when every variable has been assigned.

This is the stopping condition for the recursive solver.

#### `select_unassigned_variable(assignment, domains)`

Chooses the next variable to branch on.

If MRV is enabled, it selects the variable with the smallest remaining domain. If there is a tie, it uses a degree-based tie-break that prefers the variable connected to the most still-unassigned neighbors.

If MRV is disabled, it simply takes the first unassigned variable.

#### `order_domain_values(var, assignment, domains)`

Determines the order in which values should be tried.

If LCV is enabled, values are sorted by how few conflicts they cause in neighboring domains. If disabled, the current domain order is used directly.

#### `forward_check(var, value, assignment, domains)`

After assigning a value, this method removes incompatible values from neighboring domains.

This is an important pruning step because it can detect dead ends early instead of waiting for them to appear deeper in recursion.


#### `backtrack(assignment, domains)`

This is the recursive depth-first search procedure.

It:

1. checks whether the assignment is complete,
2. selects the next variable,
3. orders candidate values,
4. tests consistency,
5. assigns a value,
6. optionally performs forward checking,
7. recursively continues,
8. undoes the assignment if the branch fails.

This method is where all heuristics come together.

#### `ac3()`

Runs arc-consistency preprocessing using a queue of arcs `(variable, neighbor)`.

The purpose is to shrink domains before backtracking starts. For tightly constrained problems like Sudoku, this can significantly reduce the search space.

#### `revise(var, neighbor)`

Supports AC-3 by removing values from `var`’s domain that have no supporting value in the neighbor’s domain.

If a domain becomes empty, the problem is unsatisfiable under the current state.

#### `solve()`

The public entry point for the solver.

It resets counters, preloads already-fixed variables from singleton domains, optionally runs AC-3, and then launches recursive backtracking.

This file is reusable because it does not hardcode any problem-specific logic. The only requirement is that the caller provides:

* the variable list,
* domains,
* neighbors,
* and a valid constraint function.

That makes it easy to plug in more CSP problems later, such as n-queens, scheduling, cryptarithmetic, or graph coloring.

---

## `sudoku_instance.py`

This file defines Sudoku as a CSP instance.

### Responsibilities

It converts Sudoku into the four components required by the generic solver:

#### `sudoku_variables`

A list of all 81 cells in the grid, represented as `(row, col)` tuples.

Each cell is treated as one CSP variable.

#### `sudoku_domains(board)`

Builds the domain dictionary for a specific puzzle board.

* If a cell is empty (`"."`), its domain is `{1,2,3,4,5,6,7,8,9}`.
* If a cell is prefilled, its domain is a singleton set containing that fixed number.

This is how clues are encoded into the solver.

#### `build_sudoku_neighbors()`

Precomputes all neighboring cells for every position in the board.

A cell’s neighbors are all cells in the same:

* row,
* column,
* 3×3 box.

This creates the Sudoku constraint graph.

#### `sudoku_neighbors`

Stores the output of `build_sudoku_neighbors()` so the neighbor graph is built once and reused.

#### `different_values_constraint(cell1, val1, cell2, val2)`

Defines the Sudoku rule that neighboring cells must not share the same value.

The generic solver calls this function whenever it needs to test compatibility.

This file contains **only Sudoku knowledge**. It does not know how search works; it only describes the puzzle structure. That keeps the system modular.

---

## `sudoku_puzzles.py`

This file contains the actual Sudoku boards used by the program.

### Responsibilities

It defines `SUDOKU_PUZZLES`, a dictionary grouped by difficulty:

* `easy`
* `medium`
* `hard`

Each entry contains:

* a puzzle `name`,
* a 9×9 `board`.
This separation is important because puzzle data is not solver logic.

Keeping boards outside the engine makes the project easier to:

* test,
* expand with new puzzles,
* compare difficulty levels,
* run batch experiments across multiple inputs.

It also supports the assignment requirement to include multiple Sudoku instances.

---

## `map_coloring_instance.py`

This file defines the map coloring problem as a CSP instance.

### Responsibilities

#### `map_colors`

The available color values.

#### `map_variables`

The regions of the map, such as `WA`, `NT`, `SA`, and so on.

Each region is one CSP variable.

#### `map_domains`

The domain for each region, initially containing all available colors.

#### `map_neighbors`

The adjacency graph of the map.

If two regions share a border, they are neighbors and therefore cannot have the same color.

#### `different_colors_constraint(region1, color1, region2, color2)`

Defines the pairwise rule that adjacent regions must use different colors.

This file proves that the solver is truly generic.

Sudoku is a dense, highly constrained grid problem, while map coloring is a small graph-coloring problem. Since both are expressed with the same CSP interface, the solver can handle both without changing its internal logic.

---

## `run_sudoku.py`

This file is the Sudoku runner.

### Responsibilities

It imports:

* the generic `CSP` engine,
* Sudoku variables/domains/neighbors/constraint,
* the predefined Sudoku puzzle set.

It also defines a set of solver configurations so the same puzzle can be solved with different heuristics.

### Configuration design

The runner uses named configurations such as:

* Baseline
* MRV
* MRV + FC
* MRV + FC + LCV

These are passed into the `CSP` constructor as keyword arguments.

This is a good experimental design because it cleanly separates:

* the problem itself,
* the solver options used to solve it.

That makes it easy to compare performance and behavior.

### Runtime flow

For each configuration and each Sudoku puzzle, the file:

1. builds a domain dictionary from the puzzle board,
2. creates a `CSP` instance,
3. calls `solve()`,
4. validates the returned solution,
5. prints the solved board.
This script is the integration point between problem data and the solver engine for Sudoku.

---

## `run_map.py`

This file is the map-coloring runner.

### Responsibilities

It follows the same overall structure as the Sudoku runner, but for map coloring.

It:

1. imports the generic solver,
2. imports the map-coloring problem definition,
3. defines heuristic configurations,
4. constructs a `CSP` object,
5. solves the instance,
6. validates and prints the solution.


---

## `run_csp.py`

This file acts as the main command-line dispatcher.

### Responsibilities

It parses command-line arguments:

* `--problem`
* `--instance`
* `--config`

Then it decides which problem runner to call:

* Sudoku runner for `--problem sudoku`
* Map runner for `--problem map`
Without this file, users would have to manually run different scripts for each problem type.

With this dispatcher, the system has one common entry point, which is better for:

* usability,
* testing,
* repeatable experiments,
* cleaner project structure.

---

## End-to-End Interaction Between Files

Here is the full flow of control through the system.

### Sudoku flow

1. A user runs the program through `run_csp.py`.
2. `run_csp.py` selects the Sudoku path.
3. `run_sudoku.py` reads a Sudoku board from `sudoku_puzzles.py`.
4. `sudoku_instance.py` converts that board into:

   * variables,
   * domains,
   * neighbors,
   * a constraint function.
5. `run_sudoku.py` creates a `CSP` object from `generic_csp.py`.
6. `generic_csp.py` optionally applies AC-3, then runs backtracking with heuristics.
7. The solution is returned to `run_sudoku.py`.
8. The runner validates and prints the solved board.

### Map coloring flow

1. A user runs the program through `run_csp.py`.
2. `run_csp.py` selects the map path.
3. `map_coloring_instance.py` provides:

   * variables,
   * domains,
   * neighbors,
   * the constraint function.
4. `run_map.py` creates a `CSP` object.
5. `generic_csp.py` solves the problem using the same backtracking engine.
6. The solution is returned to `run_map.py`.
7. The runner validates and prints the region-color assignments.

---

## Search Strategy Design

The solver combines several CSP techniques:

### Backtracking search

The base algorithm explores assignments depth-first and undoes choices when it hits a contradiction.

### MRV

Chooses the variable with the fewest legal values left.
This usually reduces branching by attacking the hardest part of the problem first.

### Degree heuristic tie-break

When MRV ties, the solver prefers the variable involved in the most remaining constraints.
This increases the chance of making a useful early decision.

### LCV

Tries the least constraining value first.
This attempts to preserve flexibility for future assignments.

### Forward checking

After making an assignment, the solver removes incompatible values from neighboring domains.
This catches impossible branches early.

### AC-3

Runs before search to enforce arc consistency across the network.
This can shrink domains substantially before recursion begins.

Together, these features make the solver much more efficient than plain brute-force search.

---

## Validation Design

Both runner files include a validation function.

This is a smart design choice because it separates:

* “the solver returned something”
  from
* “the returned result actually satisfies the problem.”

For Sudoku, validation checks rows, columns, and boxes.
For map coloring, validation checks adjacent regions.

This gives an extra correctness layer outside of the solver itself.

---

## Extensibility

The framework is built so that new CSPs can be added with minimal work.

To add another problem, you would typically create:

1. a new instance-definition file,
2. optionally a new input-data file,
3. a runner that builds a `CSP` object,
4. a dispatcher branch in `run_csp.py`.

As long as the new problem supplies:

* variables,
* domains,
* neighbors,
* constraint function,

the existing `CSP` engine can solve it.

---

## Strengths of the Current Design

* Clear separation between engine, problem modeling, data, and execution
* Reusable generic solver
* Heuristic toggles allow controlled experimentation
* Works across multiple CSP domains
* Preprocessing and pruning improve performance
* Easy to extend with new CSP instances
* Validation functions provide a correctness check

---

## Potential Improvements

A few areas could make the design even stronger:

### 1. Standardize runner interfaces

Make sure `run_sudoku.py` and `run_map.py` both expose consistent callable functions if `run_csp.py` depends on them.

### 2. Centralize configuration handling

Instead of repeating the same configuration list in multiple runner files, move configurations into a shared file.


### 3. Reduce duplication between runners

The runner files share a lot of orchestration logic. A shared experiment helper could reduce repeated code.

---

## Conclusion

This project is a well-structured example of a generic CSP architecture.

The system works because it cleanly separates:

* **what the problem is** from
* **how the problem is solved**.

`generic_csp.py` provides the reusable search engine.
`sudoku_instance.py` and `map_coloring_instance.py` translate real problems into CSP form.
`sudoku_puzzles.py` supplies concrete Sudoku inputs.
`run_sudoku.py`, `run_map.py`, and `run_csp.py` orchestrate execution.

That design makes the framework easier to understand, test, maintain, and extend.

---

## Project Structure

```text
project/src/csp
│
├── generic_csp.py             # Generic CSP engine
├── sudoku_instance.py         # Sudoku modeled as CSP
├── sudoku_puzzles.py          # Sudoku boards grouped by difficulty
├── map_coloring_instance.py   # Map coloring modeled as CSP
├── run_sudoku.py              # Sudoku experiment runner
├── run_map.py                 # Map coloring experiment runner
└── run_csp.py                 # Main CLI dispatcher
```

---

# AI Disclosure

AI tools were used during the development of this project as a supporting resource for explanation, debugging, and documentation, but not as a direct substitute for implementing the core algorithms.

The primary uses of AI assistance included:

Clarifying conceptual questions about constraint satisfaction problems, including MRV, forward checking, LCV, and AC-3.

Explaining expected behaviors of heuristics and how they affect the search tree.

Assisting with structuring written explanations for the experiment analysis section of the report.

Providing suggestions for code organization, debugging strategies, and logging mechanisms (e.g., capturing a domain wipe-out example).

Helping format experiment outputs into Markdown tables for inclusion in the report.

During this project, AI tools were used to assist with explanations, debugging guidance, and report writing. Example prompts included:

Requests for explanations of CSP techniques such as Minimum Remaining Values (MRV), Forward Checking, Least Constraining Value (LCV), and AC-3.

Requests for clarification on how forward checking detects domain wipe-outs and how to demonstrate this in a report.

Requests to format experiment results into Markdown tables for documentation.