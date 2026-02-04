import time
from grid import move
from node import ExtractPath, Node
from collections import deque


def Succ(state, m, n):
    actions = ["U", "D", "L", "R"]
    successors = []

    for action in actions:
        next_state = move(state, action)

        # if next state is inside grid: add to successors
        if 0 <= next_state[0] < m and 0 <= next_state[1] < n:
            successors.append((action, next_state))

    return successors

def DFS(s0, goal, m, n):

    start_ns = time.perf_counter_ns()

    # 1: frontier <- Stack()
    frontier = deque()

    # 2: frontier.push(Node(s0, nil, nil, g = 0))
    frontier.append(Node(s0, None, None, 0))

    # 3: explored <- ∅
    explored = set()

    expanded_states = 0
    generated_nodes = 1     # start node
    max_frontier_size = len(frontier)

    # 4: while frontier not empty do
    while frontier:

        # 5: n <- frontier.pop()
        node = frontier.pop()

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
                        "status": "success"
                    }) 
        
        # 8: if n.state ∉ explored then
        if node.state not in explored:

            # 9: add n.state to explored
            explored.add(node.state)
            expanded_states += 1


            # 10: for all (a, s′) belongs to Succ(n.state) do
            for (action, next_state) in Succ(node.state, m, n):
                generated_nodes += 1

                # 11: frontier.push(Node(s′, n, a, g = n.g + 1))
                frontier.append(Node(next_state, node, action, node.g + 1))
                if len(frontier) > max_frontier_size:
                    max_frontier_size = len(frontier)

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