import math


def manhattan(state, goal):
    r, c = state
    rg, cg = goal
    return abs(r - rg) + abs(c - cg)


def euclidean(state, goal):
    r, c = state
    rg, cg = goal
    return math.sqrt((r - rg) ** 2 + (c - cg) ** 2)
