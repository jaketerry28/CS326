import time

from .generic_csp import CSP
from .sudoku_instance import (
    sudoku_variables,
    sudoku_domains,
    sudoku_neighbors,
    different_values_constraint,
)
from .sudoku_puzzles import SUDOKU_PUZZLES


CONFIGURATIONS = {
    "baseline": {"use_mrv": False, "use_forward_checking": False, "use_lcv": False},
    "mrv": {"use_mrv": True, "use_forward_checking": False, "use_lcv": False},
    "mrv fc": {"use_mrv": True, "use_forward_checking": True, "use_lcv": False},
    "mrv fc lcv": {"use_mrv": True, "use_forward_checking": True, "use_lcv": True},
}


def get_sudoku_instance(instance_name):
    for difficulty, puzzles in SUDOKU_PUZZLES.items():
        for puzzle in puzzles:
            if puzzle["name"] == instance_name:
                return puzzle
    raise ValueError(f"Unknown sudoku instance: {instance_name}")


def validate_solution(solution):
    if solution is None:
        return False

    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for (r, c), val in solution.items():
        box = (r // 3) * 3 + (c // 3)

        if val in rows[r] or val in cols[c] or val in boxes[box]:
            return False

        rows[r].add(val)
        cols[c].add(val)
        boxes[box].add(val)

    return True


def format_sudoku_solution(solution):
    if solution is None:
        return None

    return [[solution[(r, c)] for c in range(9)] for r in range(9)]


def run_sudoku(instance, config):
    config_key = config.lower()

    if config_key not in CONFIGURATIONS:
        raise ValueError(f"Unknown config: {config}")

    puzzle = get_sudoku_instance(instance)

    csp = CSP(
        variables=sudoku_variables,
        domains=sudoku_domains(puzzle["board"]),
        neighbors=sudoku_neighbors,
        constraint=different_values_constraint,
        **CONFIGURATIONS[config_key],
    )

    start = time.perf_counter()
    solution = csp.solve()
    end = time.perf_counter()

    solved = solution is not None and validate_solution(solution)

    return {
        "problem": "sudoku",
        "instance": instance,
        "config": config,
        "solved": solved,
        "runtime_ms": (end - start) * 1000,
        "assignments_tried": csp.assignments_tried,
        "backtracks": csp.backtracks,
        "solution": format_sudoku_solution(solution),
    }