# test_generic_csp.py

from copy import deepcopy
from csp.generic_csp import CSP


def not_equal_constraint(var1, val1, var2, val2):
    """Simple binary constraint: neighboring variables must differ."""
    return val1 != val2


def make_simple_csp(domains=None, **kwargs):
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
        **kwargs,
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
    csp = make_simple_csp(domains, use_mrv=True)
    assignment = {}

    assert csp.select_unassigned_variable(assignment, csp.domains) == "B"


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

    csp = CSP(
        variables=variables,
        domains=deepcopy(domains),
        neighbors=neighbors,
        constraint=not_equal_constraint,
        use_mrv=True,
    )
    assignment = {}

    assert csp.select_unassigned_variable(assignment, csp.domains) == "B"


def test_order_domain_values_returns_domain_values():
    csp = make_simple_csp(use_lcv=False)
    values = csp.order_domain_values("A", {}, csp.domains)

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

    csp = CSP(
        ["A", "B", "C"],
        deepcopy(domains),
        neighbors,
        not_equal_constraint,
        use_lcv=True,
    )

    ordered = csp.order_domain_values("A", {}, csp.domains)

    assert ordered == [2, 1]


def test_prune_value_removes_value_and_logs_change():
    csp = make_simple_csp()
    domains = deepcopy(csp.domains)
    pruned = []

    csp.prune_value(domains, "A", 1, pruned)

    assert domains["A"] == {2}
    assert pruned == [("A", 1)]


def test_restore_restores_pruned_values():
    csp = make_simple_csp()
    domains = deepcopy(csp.domains)
    pruned = []

    csp.prune_value(domains, "A", 1, pruned)
    csp.prune_value(domains, "B", 2, pruned)
    csp.restore(domains, pruned)

    assert domains["A"] == {1, 2}
    assert domains["B"] == {1, 2}


def test_assign_prunes_other_values_from_assigned_variable():
    csp = make_simple_csp()
    domains = deepcopy(csp.domains)
    pruned = []

    csp.assign("A", 1, domains, pruned)

    assert domains["A"] == {1}
    assert ("A", 2) in pruned


def test_forward_check_prunes_neighbor_domains():
    csp = make_simple_csp()
    domains = deepcopy(csp.domains)
    assignment = {"A": 1}
    pruned = []

    result = csp.forward_check("A", 1, assignment, domains, pruned)

    assert result is True
    assert domains["B"] == {2}
    assert ("B", 1) in pruned


def test_forward_check_returns_false_when_domain_becomes_empty():
    domains = {
        "A": {1},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    working_domains = deepcopy(csp.domains)
    assignment = {"A": 1}
    pruned = []

    result = csp.forward_check("A", 1, assignment, working_domains, pruned)

    assert result is False
    assert working_domains["B"] == set()
    assert ("B", 1) in pruned


def test_revise_removes_unsupported_values():
    domains = {
        "A": {1, 2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    working_domains = deepcopy(csp.domains)

    revised = csp.revise(working_domains, "A", "B")

    assert revised is True
    assert working_domains["A"] == {2}


def test_revise_returns_false_when_no_change_needed():
    domains = {
        "A": {2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    working_domains = deepcopy(csp.domains)

    revised = csp.revise(working_domains, "A", "B")

    assert revised is False
    assert working_domains["A"] == {2}


def test_ac3_returns_true_when_consistent():
    domains = {
        "A": {1, 2},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    working_domains = deepcopy(csp.domains)

    result = csp.ac3(working_domains)

    assert result is True
    assert working_domains["A"] == {2}
    assert working_domains["B"] == {1}
    assert working_domains["C"] == {2}

def test_ac3_returns_false_when_inconsistent():
    domains = {
        "A": {1},
        "B": {1},
        "C": {1, 2},
    }
    csp = make_simple_csp(domains)
    working_domains = deepcopy(csp.domains)

    result = csp.ac3(working_domains)

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