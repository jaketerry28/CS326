import heapq
import time

from .node import Node, ExtractPath
from .grid import move, in_bounds, ACTIONS



# Yield (action, next_state, step_cost) for legal moves only.
def successors(state, m, n, costs):
    for a in ACTIONS:
        s2 = move(state, a)
        if in_bounds(s2, m, n) and (state, a) in costs:
            yield a, s2, costs[(state, a)]


def astar(m, n, start, goal, costs, heuristic_fn):

    t0 = time.perf_counter()

    # 1: frontier ← PriorityQueue(by f)
    frontier = []
    tie = 0

    # 2: frontier.push(Node(s0, nil, nil, g = 0))
    h0 = heuristic_fn(start, goal)
    start_node = Node(state=start, parent=None, action=None, g=0, h=h0, tie=tie)
    heapq.heappush(frontier, (start_node.f, start_node.tie, start_node))
    tie += 1

    # 3: bestCost ← empty map
    bestCost = {}

    # Metrics tracking
    expanded_states = 0
    generated_nodes = 1
    max_frontier_size = 1

    # 4: while frontier not empty do
    while frontier:

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)

        # 5: n ← frontier.pop()
        _, _, node = heapq.heappop(frontier)

        # 6: if Goal(n.state) then return ExtractPath(n)
        if node.state == goal:
            states, actions = ExtractPath(node)
            runtime_ms = (time.perf_counter() - t0) * 1000.0
            return {
                "status": "success",
                "states": states,
                "actions": actions,
                "steps": len(actions),
                "total_cost": node.g,
                "expanded_states": expanded_states,
                "generated_nodes": generated_nodes,
                "max_frontier_size": max_frontier_size,
                "runtime_ms": runtime_ms,
            }

        expanded_states += 1

        # 8: if n.state ∉ bestCost or n.g < bestCost[n.state] then
        if (node.state not in bestCost) or (node.g < bestCost[node.state]):

            # 9: bestCost[n.state] ← n.g
            bestCost[node.state] = node.g

            # 10: for all (a, s′, cost) ∈ Succ(n.state) do
            for a, s2, step_cost in successors(node.state, m, n, costs):

                # 11: g′ ← n.g + cost
                g2 = node.g + step_cost

                # 12: frontier.push(Node(s′, n, a, g = g′))
                h2 = heuristic_fn(s2, goal)
                child = Node(state=s2, parent=node, action=a, g=g2, h=h2, tie=tie)
                heapq.heappush(frontier, (child.f, child.tie, child))
                tie += 1
                generated_nodes += 1

        # 14: end if
    # 15: end while

    # 16: return failure
    runtime_ms = (time.perf_counter() - t0) * 1000.0
    return {
        "status": "failure",
        "states": [],
        "actions": [],
        "steps": 0,
        "total_cost": None,
        "expanded_states": expanded_states,
        "generated_nodes": generated_nodes,
        "max_frontier_size": max_frontier_size,
        "runtime_ms": runtime_ms,
    }
