from copy import deepcopy

from csp.generic_csp import CSP
from csp.map_coloring_instance import (
    map_variables,
    map_domains,
    map_neighbors,
    different_colors_constraint,
)
from csp.run_map import validate_solution


def test_map_coloring_solution_is_valid():
    """
    Requirement checks:
    • Every region has a color assigned
    • Every edge (u,v) satisfies color(u) != color(v)
    """

    csp = CSP(
        variables=map_variables,
        domains=deepcopy(map_domains),
        neighbors=map_neighbors,
        constraint=different_colors_constraint,
    )

    solution = csp.solve()

    assert solution is not None

    # Reuse validation helper
    assert validate_solution(solution) is True