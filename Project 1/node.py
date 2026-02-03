class Node:
    def __init__(self, state, parent, action, g):
        self.state = state # (row, column)
        self.parent = parent    # parent Node
        self.action = action    # U, D, L, R
        self.g = g          # cost to reach this node from start


def ExtractPath(node):

    # get the path from end to beginning
    states = []
    actions = []
    current = node

    while current is not None:
        states.append(current.state)
        actions.append(current.action)
        current = current.parent
    
    # reverse the path to get from beginning to end
    states.reverse()
    actions.reverse()

    return (states, actions[1:]) # exclude the first action which is None
