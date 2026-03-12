
"""
sudoku_instance.py

Defines variables, domains, constraints for a Sudoku CSP instance.

Variables: Each cell in the Sudoku grid is a variable, represented as a tuple (row, column).
Domains: Each variable can take on values from 1 to 9.
Constraints: No row, column, or box can have duplicate values.

"""

from typing import Dict, List, Set, Tuple


# There are 81 variables (cells) in a 9x9 Sudoku grid
sudoku_variables = [(r, c) for r in range(9) for c in range(9)]


def sudoku_domains(board: List[List[str]]) -> Dict[Tuple[int, int], Set[int]]:
    domains = {}

    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                domains[(r, c)] = set(range(1, 10))
            else:
                domains[(r, c)] = {int(board[r][c])}

    return domains



def build_sudoku_neighbors():
    neighbors = {}

    for r in range(9):
        for c in range(9):
            cell = (r, c)

            row = {(r, cc) for cc in range(9) if cc != c}
            col = {(rr, c) for rr in range(9) if rr != r}

            box_r, box_c = 3 * (r // 3), 3 * (c // 3)
            box = {
                (rr, cc)
                for rr in range(box_r, box_r + 3)
                for cc in range(box_c, box_c + 3)
                if (rr, cc) != cell
            }

            neighbors[cell] = list(row | col | box)

    return neighbors

sudoku_neighbors = build_sudoku_neighbors()



def different_values_constraint(cell1, val1, cell2, val2):
    if cell2 in sudoku_neighbors[cell1]:
        return val1 != val2
    return True
