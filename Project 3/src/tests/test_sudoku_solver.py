from copy import deepcopy

from csp.generic_csp import CSP
from csp.sudoku_instance import (
    sudoku_variables,
    sudoku_domains,
    sudoku_neighbors,
    different_values_constraint,
)
from csp.sudoku_puzzles import SUDOKU_PUZZLES
from csp.run_sudoku import validate_solution


def test_sudoku_solution_is_complete_and_valid():
    """
    Requirement checks:
    • Grid is complete when solved=True (no zeros)
    • Rows/columns/blocks contain digits 1–9 with no repetition
    """

    puzzle = deepcopy(SUDOKU_PUZZLES["easy"][0]["board"])

    csp = CSP(
        variables=sudoku_variables,
        domains=sudoku_domains(puzzle),
        neighbors=sudoku_neighbors,
        constraint=different_values_constraint,
    )

    solution = csp.solve()

    assert solution is not None

    # Use existing validation helper
    assert validate_solution(solution) is True