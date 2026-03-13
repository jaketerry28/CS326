# Generic CSP Solver

Each instance of a CSP is defined by a set of variables, a set of domains for each variable, and a set of constraints that specify which combinations of variable assignments are valid.

## Map Coloring Problem

The map coloring problem is a classic example of a CSP. The goal is to color a map using a limited number of colors such that no two adjacent regions share the same color.

In this project, we will implement a CSP solver to solve the map coloring problem for the map of Australia. The variables represent the regions of Australia, the domains represent the colors that can be used to color each region, and the constraints ensure that adjacent regions do not share the same color.

## Sudoku Problem

The Sudoku problem is another example of a CSP. The goal is to fill a 9x9 grid with digits from 1 to 9 such that each row, column, and 3x3 subgrid contains all the digits from 1 to 9 without repetition.

In this project, we will also implement a CSP solver to solve Sudoku puzzles. The variables represent the cells in the grid, the domains represent the possible digits that can be assigned to each cell, and the constraints ensure that no digit is repeated in any row, column, or 3x3 subgrid.

## How to Run the Code

To run the code, use the following command in the terminal, replacing `<problem>`, `<instance>`, and `<config>` with the appropriate values for the problem you want to solve:

```
python -m csp.run_csp --problem <problem> --instance <instance> --config <config>
```

### Map Coloring

```
python -m csp.run_csp --problem map --instance australia --config baseline
python -m csp.run_csp --problem map --instance australia --config mrv
python -m csp.run_csp --problem map --instance australia --config "mrv fc"
python -m csp.run_csp --problem map --instance australia --config "mrv fc lcv"
```

### Sudoku

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