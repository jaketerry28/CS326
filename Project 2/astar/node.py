class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0, tie=0):
        self.state = state          # (row, col)
        self.parent = parent        # parent Node
        self.action = action        # U, D, L, R (action from parent -> this)
        self.g = g                  # cost-so-far
        self.h = h                  # heuristic
        self.f = g + h              # f = g + h
        self.tie = tie              # tie-breaker for heap ordering


def ExtractPath(node):
    states = []
    actions = []
    cur = node

    while cur is not None:
        states.append(cur.state)
        actions.append(cur.action)
        cur = cur.parent

    states.reverse()
    actions.reverse()

    # first action is None for the start node
    return states, actions[1:]
