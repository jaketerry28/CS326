# Tic-Tac-Toe

This module implements the Tic-Tac-Toe half of Project 4 as a separate package under `tic-tac-toe`.

## Structure

- `src/tic_tac_toe/game.py`: board state, legal moves, terminal tests, utility
- `src/tic_tac_toe/minimax.py`: Minimax and Alpha-Beta search agents
- `src/tic_tac_toe/opponents.py`: random and scripted opponents
- `src/tic_tac_toe/run_tictactoe.py`: CLI runner and JSON output
- `src/tests/test_tictactoe.py`: baseline tests

## Run

From `Project-4/tic-tac-toe/src`:

```bash
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance random --config minimax
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance scripted --config minimax
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance scripted --config alphabeta
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance random --config alphabeta
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance random --config minimax --games 10 --seed 0
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance random --config alphabeta --games 10 --seed 0
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance scripted --config minimax --games 5 --seed 100
python3 -m tic_tac_toe.run_tictactoe --problem tictactoe --instance scripted --config alphabeta --games 5 --seed 100
```

The runner prints a terminal summary and saves JSON output in `../results/`.

## Tests

From `Project-4/tic-tac-toe/src`:

```bash
python -m pytest -q
```
