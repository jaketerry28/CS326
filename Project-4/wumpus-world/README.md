# Wumpus World

This module implements the Wumpus World half of Project 4 as a separate package under `wumpus-world`.

## Structure

- `src/wumpus_world/layouts.py`: required Wumpus layouts
- `src/wumpus_world/environment.py`: grid world and percept generation
- `src/wumpus_world/knowledge_base.py`: explicit facts and inference rules
- `src/wumpus_world/agent.py`: knowledge-based agent loop
- `src/wumpus_world/run_wumpus.py`: CLI runner and JSON output
- `src/tests/test_wumpus_world.py`: baseline tests

## Run

From `Project 4/wumpus-world/src`:

```bash
python3 -m wumpus_world.run_wumpus --problem wumpus --instance easy_1 --config kb
python3 -m wumpus_world.run_wumpus --problem wumpus --instance easy_2 --config kb
python3 -m wumpus_world.run_wumpus --problem wumpus --instance hard_1 --config kb
python3 -m wumpus_world.run_wumpus --problem wumpus --instance hard_2 --config kb
```

The runner prints a terminal summary and saves a JSON file in `../results/`.

## Tests

From `Project 4/wumpus-world/src`:

```bash
python -m pytest -q
```
