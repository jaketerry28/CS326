
"""
sudoku_instance.py

Defines variables, domains, constraints for a Sudoku CSP instance.

Variables: Each cell in the Sudoku grid is a variable, represented as a tuple (row, column).
Domains: Each variable can take on values from 1 to 9.
Constraints: No row, column, or box can have duplicate values.

"""

from typing import List


# There are 81 variables (cells) in a 9x9 Sudoku grid
sudoku_variables = [(r, c) for r in range(9) for c in range(9)]

# If a cell is blank: D(Xr,c) = {1, . . . , 9}
# If a cell is pre-filled with k: D(Xr,c) = {k}.
sudoku_domains = {(r,c): set(range(1, 10)) for r in range(9) for c in range(9)}


# Constraints: No two variables in the same row, column, or box can have the same value.
def is_different_constraint(board: List[List[str]]) -> bool:
    # bit masking to check for duplicates in rows, columns, and 3x3 boxes
    rows = [0] * 9
    cols = [0] * 9
    squares = [0] * 9

    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                continue

            val = int(board[r][c]) - 1
            if (1 << val) & rows[r]:
                return False
            if (1 << val) & cols[c]:
                return False
            if (1 << val) & squares[(r // 3) * 3 + (c // 3)]:
                return False

            rows[r] |= (1 << val)
            cols[c] |= (1 << val)
            squares[(r // 3) * 3 + (c // 3)] |= (1 << val)

    return True