import random


def buildCosts(m, n, min_cost, max_cost, seed):
    random.seed(seed)
    actions = ["U", "D", "L", "R"] # Order is important for reproducibility

    costs = {}

    for r in range(m):
        for c in range(n):

            state = (r, c)
            
            for action in actions:
                next_state = move(state, action)
                
                # if next state is inside grid: assign random cost
                if 0 <= next_state[0] < m and 0 <= next_state[1] < n:
                    costs[(state, action)] = random.randint(min_cost, max_cost)
    return costs
             

def move(state, action):
    (r, c) = state

    if action == "U":
        return (r+1, c)
    elif action == "D":
        return (r-1, c)
    elif action == "L":
        return (r, c-1)
    elif action == "R":
        return (r, c+1)
    else:
        raise ValueError("Invalid action: {}".format(action))
    