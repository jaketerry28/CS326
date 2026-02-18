import random

ACTIONS = ["U", "D", "L", "R"]  # order matters for reproducibility


def move(state, action):
    """Standard grid convention: row decreases when moving Up."""
    r, c = state
    if action == "U":
        return (r - 1, c)
    if action == "D":
        return (r + 1, c)
    if action == "L":
        return (r, c - 1)
    if action == "R":
        return (r, c + 1)
    raise ValueError(f"Unknown action: {action}")


def in_bounds(state, m, n):
    r, c = state
    return 0 <= r < m and 0 <= c < n


def buildCosts(m, n, min_cost, max_cost, seed):
    """
    Builds directed edge costs: costs[(state, action)] -> int
    Only includes legal (in-bounds) moves.
    """
    random.seed(seed)

    costs = {}
    for r in range(m):
        for c in range(n):
            s = (r, c)
            for a in ACTIONS:
                s2 = move(s, a)
                if in_bounds(s2, m, n):
                    costs[(s, a)] = random.randint(min_cost, max_cost)
    return costs
