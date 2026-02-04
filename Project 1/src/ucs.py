import time
from grid import move
from node import ExtractPath, Node
from collections import deque
import heapq
from itertools import count

def Succ(state, m, n):
    actions = ["U", "D", "L", "R"]
    successors = []

    for action in actions:
        next_state = move(state, action)

        # if next state is inside grid: add to successors
        if 0 <= next_state[0] < m and 0 <= next_state[1] < n:
            successors.append((action, next_state))

    return successors

def UCS(s0, goal, m, n, costs):

    start_ns = time.perf_counter_ns()
    counter = count()

    # 1: frontier ← PriorityQueue(by g )
    frontier = []

    # 2: frontier .push(Node(s0, nil, nil, g = 0))
    heapq.heappush(frontier, (0, next(counter), Node(s0, None, None, 0)))

    # 3: bestCost ← empty map
    bestCost = {}

    expanded_states = 0
    generated_nodes = 1     # start node
    max_frontier_size = len(frontier)

    # 4: while frontier not empty do
    while frontier:

        # 5: n ← frontier .pop()
        g, tie_breaker, node = heapq.heappop(frontier) # get the node with lowest g

        # 6: if Goal(n.state) then return ExtractPath(n)
        if node.state == goal:

            states, actions = ExtractPath(node)
            runtime_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            return (states,
                    actions,
                    {
                        "expanded_states": expanded_states,
                        "generated_nodes": generated_nodes,
                        "max_frontier_size": max_frontier_size,
                        "runtime_ms": runtime_ms,
                        "status": "success",
                        "total_cost": node.g

                    })
        # 7: end if

        # 8: if n.state /∈ bestCost or n.g < bestCost[n.state] then
        if (node.state not in bestCost) or (node.g < bestCost[node.state]):

            # 9: bestCost[n.state] ← n.g
            bestCost[node.state] = node.g
            expanded_states += 1

            # 10: for all (a, s′, cost) ∈ Succ(n.state) do
            for (action, next_state) in Succ(node.state, m, n):
                new_g = node.g + costs[(node.state, action)]

                child = Node(next_state, node, action, new_g)

                # 11: frontier .push(Node(s′, n, a, g = n.g + cost))
                heapq.heappush(frontier, (child.g, next(counter), child))
                generated_nodes += 1

                if len(frontier) > max_frontier_size:
                    max_frontier_size = len(frontier)
            # 12: end for
        # 13: end if
    # 14: end while

    # 15: return failure
    runtime_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
    return ([],
            [],
            {
                "expanded_states": expanded_states,
                "generated_nodes": generated_nodes,
                "max_frontier_size": max_frontier_size,
                "runtime_ms": runtime_ms,
                "status": "failure"
            })