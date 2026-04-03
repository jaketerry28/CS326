# CS 326 Project 4

This project contains two separate AI systems for Project 4:

- `wumpus-world/`: a knowledge-based Wumpus World agent
- `tic-tac-toe/`: a Tic-Tac-Toe agent using Minimax and Alpha-Beta pruning

The submission also includes:

- `REPORT.md`: the written report draft
- `SUBMISSION_CHECKLIST.md`: submission tracking checklist
- `plots/`: generated figures for the report

## Project Structure

```text
Project-4/
├── README.md
├── REPORT.md
├── SUBMISSION_CHECKLIST.md
├── plots/
├── wumpus-world/
│   ├── README.md
│   ├── results/
│   └── src/
└── tic-tac-toe/
    ├── README.md
    ├── results/
    └── src/
```

## Wumpus World

From `Project-4/wumpus-world/src`:

```bash
python -m wumpus_world.run_wumpus --problem wumpus --instance easy_1 --config kb
python -m wumpus_world.run_wumpus --problem wumpus --instance easy_2 --config kb
python -m wumpus_world.run_wumpus --problem wumpus --instance hard_1 --config kb
python -m wumpus_world.run_wumpus --problem wumpus --instance hard_2 --config kb
python -m pytest -q
```

Results are written to `Project-4/wumpus-world/results/`.

## Tic-Tac-Toe

From `Project-4/tic-tac-toe/src`:

```bash
python -m tic_tac_toe.run_tictactoe --problem tictactoe --instance random --config minimax --games 10 --seed 0
python -m tic_tac_toe.run_tictactoe --problem tictactoe --instance scripted --config minimax --games 5 --seed 100
python -m tic_tac_toe.run_tictactoe --problem tictactoe --instance random --config alphabeta --games 10 --seed 0
python -m tic_tac_toe.run_tictactoe --problem tictactoe --instance scripted --config alphabeta --games 5 --seed 100
python -m pytest -q
```

Results are written to `Project-4/tic-tac-toe/results/`.

## Plots

To regenerate the plots used in the report:

```bash
python Project-4/generate_plots.py
```

Generated images are saved in `Project-4/plots/`.

## Notes

- The Wumpus World agent uses explicit facts and inference rules, not a hard-coded move sequence.
- The Tic-Tac-Toe module includes both `minimax` and `alphabeta` configurations.
- JSON outputs for the required runs are already included in the repository.
