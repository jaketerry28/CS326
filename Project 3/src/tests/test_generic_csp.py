# test_generic_csp.py

from copy import deepcopy
from csp.generic_csp import CSP


def not_equal_constraint(var1, val1, var2, val2):
    """Simple binary constraint: neighboring variables must differ."""
    return val1 != val2


def make_simple_csp(domains=None):
    """
    A tiny generic CSP:
        A -- B -- C
    """
    variables = ["A", "B", "C"]
    default_domains = {
        "A": {1, 2},
        "B": {1, 2},
        "C": {1, 2},
    }
    neighbors = {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B"],
    }

    return CSP(
        variables=variables,
        domains=deepcopy(domains if domains is not None else default_domains),
        neighbors=neighbors,
        constraint=not_equal_constraint,
    )


def test_is_consistent_returns_true_when_assignment_valid():
    csp = make_simple_csp()
    assignment = {"A": 1}

    assert csp.is_consistent("B", 2, assignment) is True


def test_is_consistent_returns_false_when_assignment_invalid():
    csp = make_simple_csp()
    assignment = {"A": 1}

    assert csp.is_consistent("B", 1, assignment) is False


def test_is_complete_returns_false_for_partial_assignment():
    csp = make_simple_csp()
    assignment = {"A": 1}

    assert csp.is_complete(assignment) is False


def test_is_complete_returns_true_for_full_assignment():
    csp = make_simple_csp()
    assignment = {"A": 1, "B": 2, "C": 1}

    assert csp.is_complete(assignment) is True


def test_select_unassigned_variable_uses_mrv():
    domains = {
        "A": {1, 2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    assignment = {}

    assert csp.select_unassigned_variable(assignment) == "B"


def test_select_unassigned_variable_uses_degree_tiebreak():
    variables = ["A", "B", "C", "D"]
    domains = {
        "A": {1, 2},
        "B": {1, 2},
        "C": {1, 2},
        "D": {1, 2},
    }
    neighbors = {
        "A": ["B"],
        "B": ["A", "C", "D"],
        "C": ["B"],
        "D": ["B"],
    }

    csp = CSP(variables, deepcopy(domains), neighbors, not_equal_constraint)
    assignment = {}

    # all domains same size, so MRV ties
    # B has the most unassigned neighbors, so degree heuristic should pick B
    assert csp.select_unassigned_variable(assignment) == "B"


def test_order_domain_values_returns_domain_values():
    csp = make_simple_csp()
    values = csp.order_domain_values("A", {})

    assert set(values) == {1, 2}
    assert len(values) == 2


def test_order_domain_values_prefers_least_constraining_value():
    domains = {
        "A": {1, 2},
        "B": {1, 2},
        "C": {1},
    }
    neighbors = {
        "A": ["B", "C"],
        "B": ["A"],
        "C": ["A"],
    }

    csp = CSP(["A", "B", "C"], deepcopy(domains), neighbors, not_equal_constraint)

    ordered = csp.order_domain_values("A", {})

    # If A=1, it conflicts with B=1 and C=1 => 2 conflicts
    # If A=2, it conflicts only with B=2 => 1 conflict
    assert ordered == [2, 1]


def test_forward_check_prunes_neighbor_domains():
    csp = make_simple_csp()
    domains = deepcopy(csp.domains)
    assignment = {"A": 1}

    pruned = csp.forward_check("A", 1, assignment, domains)

    assert pruned is not None
    assert domains["B"] == {2}


def test_forward_check_returns_none_when_domain_becomes_empty():
    domains = {
        "A": {1},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    working_domains = deepcopy(csp.domains)
    assignment = {"A": 1}

    pruned = csp.forward_check("A", 1, assignment, working_domains)

    assert pruned is None


def test_restore_puts_pruned_values_back():
    csp = make_simple_csp()
    domains = deepcopy(csp.domains)
    assignment = {"A": 1}

    pruned = csp.forward_check("A", 1, assignment, domains)

    assert domains["B"] == {2}

    csp.restore(domains, pruned)

    assert domains["B"] == {1, 2}


def test_revise_removes_unsupported_values():
    domains = {
        "A": {1, 2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)

    revised = csp.revise("A", "B")

    assert revised is True
    assert csp.domains["A"] == {2}


def test_revise_returns_false_when_no_change_needed():
    domains = {
        "A": {2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)

    revised = csp.revise("A", "B")

    assert revised is False
    assert csp.domains["A"] == {2}


def test_ac3_returns_true_when_consistent():
    domains = {
        "A": {1, 2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)

    result = csp.ac3()

    assert result is True
    assert csp.domains["A"] == {2}


def test_ac3_returns_false_when_inconsistent():
    domains = {
        "A": {1},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)

    result = csp.ac3()

    assert result is False


def test_backtrack_finds_solution():
    csp = make_simple_csp()

    result = csp.backtrack({}, deepcopy(csp.domains))

    assert result is not None
    assert set(result.keys()) == {"A", "B", "C"}
    assert result["A"] != result["B"]
    assert result["B"] != result["C"]


def test_backtrack_returns_none_when_no_solution():
    domains = {
        "A": {1},
        "B": {1},
        "C": {1},
    }
    csp = make_simple_csp(domains)

    result = csp.backtrack({}, deepcopy(csp.domains))

    assert result is None


def test_solve_finds_solution():
    csp = make_simple_csp()

    result = csp.solve()

    assert result is not None
    assert set(result.keys()) == {"A", "B", "C"}
    assert result["A"] != result["B"]
    assert result["B"] != result["C"]


def test_solve_returns_none_when_unsatisfiable():
    domains = {
        "A": {1},
        "B": {1},
        "C": {1},
    }
    csp = make_simple_csp(domains)

    result = csp.solve()

    assert result is None