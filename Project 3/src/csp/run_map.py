import time
from copy import deepcopy

from .generic_csp import CSP
from .map_coloring_instance import (
    map_variables,
    map_domains,
    map_neighbors,
    different_colors_constraint,
)


CONFIGURATIONS = {
    "baseline": {"use_mrv": False, "use_forward_checking": False, "use_lcv": False},
    "mrv": {"use_mrv": True, "use_forward_checking": False, "use_lcv": False},
    "mrv fc": {"use_mrv": True, "use_forward_checking": True, "use_lcv": False},
    "mrv fc lcv": {"use_mrv": True, "use_forward_checking": True, "use_lcv": True},
}


def validate_solution(solution):
    if solution is None:
        return False

    for region in map_variables:
        for neighbor in map_neighbors[region]:
            if solution[region] == solution[neighbor]:
                return False
    return True


def run_map(instance, config):
    config_key = config.lower()

    if config_key not in CONFIGURATIONS:
        raise ValueError(f"Unknown config: {config}")

    # only one map instance right now, so just accept "australia"
    if instance.lower() != "australia":
        raise ValueError(f"Unknown map instance: {instance}")

    csp = CSP(
        variables=map_variables,
        domains=deepcopy(map_domains),
        neighbors=map_neighbors,
        constraint=different_colors_constraint,
        **CONFIGURATIONS[config_key],
    )

    start = time.perf_counter()
    solution = csp.solve()
    end = time.perf_counter()

    solved = solution is not None and validate_solution(solution)

    return {
        "problem": "map",
        "instance": instance,
        "config": config,
        "solved": solved,
        "runtime_ms": (end - start) * 1000,
        "assignments_tried": csp.assignments_tried,
        "backtracks": csp.backtracks,
        "solution": solution,
    }