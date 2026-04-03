from wumpus_world.agent import KnowledgeBasedWumpusAgent
from wumpus_world.environment import Percept, WumpusWorld
from wumpus_world.knowledge_base import WumpusKnowledgeBase
from wumpus_world.layouts import get_layout


def test_environment_generates_expected_percepts():
    world = WumpusWorld(get_layout("hard_2"))

    assert world.perceive((0, 0)) == Percept(breeze=False, stench=False)
    assert world.perceive((1, 1)) == Percept(breeze=True, stench=True)
    assert world.perceive((0, 2)) == Percept(breeze=True, stench=False)
    assert world.perceive((2, 0)) == Percept(breeze=False, stench=True)


def test_knowledge_base_updates_after_each_percept():
    world = WumpusWorld(get_layout("easy_1"))
    kb = WumpusKnowledgeBase(size=world.size, start=world.start)

    kb.tell_percept((0, 0), world.perceive((0, 0)))
    assert (0, 0) in kb.visited
    assert (1, 0) in kb.safe
    assert (0, 1) in kb.safe

    kb.tell_percept((1, 0), world.perceive((1, 0)))
    assert (1, 0) in kb.visited
    assert (2, 0) in kb.safe
    assert (1, 1) in kb.safe
    assert kb.percepts[(1, 0)] == Percept(breeze=False, stench=False)


def test_kb_can_isolate_hazards_from_overlapping_clues():
    world = WumpusWorld(get_layout("hard_2"))
    kb = WumpusKnowledgeBase(size=world.size, start=world.start)

    for square in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]:
        kb.tell_percept(square, world.perceive(square))

    assert kb.known_wumpus == (2, 1)
    assert (1, 2) in kb.known_pits
    assert (2, 0) in kb.visited
    assert (1, 0) in kb.safe


def test_agent_never_moves_into_square_already_known_unsafe():
    world = WumpusWorld(get_layout("hard_1"))
    agent = KnowledgeBasedWumpusAgent(world)
    result = agent.run()

    known_unsafe_so_far: set[tuple[int, int]] = set()
    for entry in result["trace"]:
        target = tuple(entry["to"])
        assert target not in known_unsafe_so_far

        knowledge = entry["knowledge"]
        known_unsafe_so_far.update(tuple(coord) for coord in knowledge["known_pits"])
        if knowledge["known_wumpus"] is not None:
            known_unsafe_so_far.add(tuple(knowledge["known_wumpus"]))


def test_agent_fully_explores_easy_layout():
    world = WumpusWorld(get_layout("easy_1"))
    agent = KnowledgeBasedWumpusAgent(world)
    result = agent.run()

    assert result["success"] is True
    assert result["fully_explored"] is True
    assert result["visited_squares"] == result["total_safe_squares"]
