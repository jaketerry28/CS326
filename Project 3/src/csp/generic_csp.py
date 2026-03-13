from collections import deque


class CSP:
    def __init__(
        self,
        variables,
        domains,
        neighbors,
        constraint,
        use_mrv=True,
        use_forward_checking=True,
        use_lcv=True,
        use_ac3=True,
    ):
        """
        Initializes the CSP problem definition.
        Stores the variables, domains for each variable, the constraint graph
        (neighbors), and the constraint function used to check validity.
        """
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraint = constraint

        self.use_mrv = use_mrv
        self.use_forward_checking = use_forward_checking
        self.use_lcv = use_lcv
        self.use_ac3 = use_ac3

        self.assignments_tried = 0
        self.backtracks = 0

    def is_consistent(self, var, value, assignment):
        """
        Checks whether assigning `value` to `var` violates any constraints.
        It compares the proposed assignment against already-assigned neighbors
        using the constraint function.
        """
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                if not self.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def is_complete(self, assignment):
        """
        Determines whether the CSP is solved.
        Returns True if every variable has been assigned a value.
        """
        return len(assignment) == len(self.variables)

    def select_unassigned_variable(self, assignment, domains):
        """
        Selects the next variable to assign using the MRV heuristic.
        Chooses the variable with the smallest remaining domain; ties are
        broken using the degree heuristic (most unassigned neighbors).
        """
        unassigned = [v for v in self.variables if v not in assignment]

        if not self.use_mrv:
            return unassigned[0]

        min_domain = min(len(domains[v]) for v in unassigned)
        candidates = [v for v in unassigned if len(domains[v]) == min_domain]

        if len(candidates) > 1:
            return max(
                candidates,
                key=lambda var: sum(1 for n in self.neighbors[var] if n not in assignment)
            )

        return candidates[0]

    def order_domain_values(self, var, assignment, domains):
        """
        Orders domain values using the LCV (Least Constraining Value) heuristic.
        Values that eliminate the fewest options for neighboring variables
        are tried first.
        """
        if not self.use_lcv:
            return list(domains[var])

        def conflicts(value):
            count = 0
            for neighbor in self.neighbors[var]:
                if neighbor not in assignment:
                    for neighbor_value in domains[neighbor]:
                        if not self.constraint(var, value, neighbor, neighbor_value):
                            count += 1
            return count

        return sorted(domains[var], key=conflicts)

    def prune_value(self, domains, var, value, pruned):
        """
        Removes a single value from a variable's domain and records it
        in the undo log so it can be restored later.
        """
        if value in domains[var]:
            domains[var].remove(value)
            pruned.append((var, value))

    def restore(self, domains, pruned):
        """
        Restores all domain values recorded in the undo log.
        Restoration is done in reverse order of pruning.
        """
        for var, value in reversed(pruned):
            domains[var].add(value)

    def assign(self, var, value, domains, pruned):
        """
        Commits var=value by pruning every other value from var's domain
        and recording those removals in the undo log.
        """
        for other_value in list(domains[var]):
            if other_value != value:
                self.prune_value(domains, var, other_value, pruned)

    def forward_check(self, var, value, assignment, domains, pruned):
        """
        Performs forward checking after assigning a value.
        Removes inconsistent values from neighbor domains and detects failure
        if any neighbor domain becomes empty.
        """
        for neighbor in self.neighbors[var]:
            if neighbor in assignment:
                continue

            for neighbor_value in list(domains[neighbor]):
                if not self.constraint(var, value, neighbor, neighbor_value):
                    self.prune_value(domains, neighbor, neighbor_value, pruned)

            if len(domains[neighbor]) == 0:
                return False

        return True

    def revise(self, domains, var, neighbor, pruned=None):
        """
        Removes values from var's domain that have no valid supporting value
        in neighbor's domain.
        """
        revised = False

        for value in list(domains[var]):
            supported = any(
                self.constraint(var, value, neighbor, neighbor_value)
                for neighbor_value in domains[neighbor]
            )

            if not supported:
                if pruned is None:
                    domains[var].remove(value)
                else:
                    self.prune_value(domains, var, value, pruned)
                revised = True

        return revised

    def ac3(self, domains, pruned=None):
        """
        Enforces arc consistency across the CSP.
        Removes values from domains that cannot satisfy constraints with neighbors.
        """
        queue = deque(
            (var, neighbor)
            for var in self.variables
            for neighbor in self.neighbors[var]
        )

        while queue:
            var, neighbor = queue.popleft()

            if self.revise(domains, var, neighbor, pruned):
                if len(domains[var]) == 0:
                    return False

                for other_neighbor in self.neighbors[var]:
                    if other_neighbor != neighbor:
                        queue.append((other_neighbor, var))

        return True

    def backtrack(self, assignment, domains):
        """
        Performs depth-first backtracking search to find a solution.
        Selects a variable, tries values in order, applies pruning,
        and recursively continues until a valid assignment is found.
        """
        if self.is_complete(assignment):
            return assignment.copy()

        var = self.select_unassigned_variable(assignment, domains)

        for value in self.order_domain_values(var, assignment, domains):
            if self.is_consistent(var, value, assignment):
                self.assignments_tried += 1

                assignment[var] = value
                pruned = []

                self.assign(var, value, domains, pruned)

                branch_ok = True

                if self.use_forward_checking:
                    branch_ok = self.forward_check(var, value, assignment, domains, pruned)

                if branch_ok:
                    result = self.backtrack(assignment, domains)
                    if result is not None:
                        return result

                self.restore(domains, pruned)
                del assignment[var]

        self.backtracks += 1
        return None

    def solve(self):
        """
        Entry point for solving the CSP.
        Runs AC-3 preprocessing and then starts backtracking search.
        """
        assignment = {}

        self.assignments_tried = 0
        self.backtracks = 0

        domains = {var: set(values) for var, values in self.domains.items()}

        for var in self.variables:
            if len(domains[var]) == 1:
                assignment[var] = next(iter(domains[var]))

        if self.use_ac3:
            if not self.ac3(domains):
                return None

            for var in self.variables:
                if len(domains[var]) == 1:
                    assignment[var] = next(iter(domains[var]))

        return self.backtrack(assignment, domains)