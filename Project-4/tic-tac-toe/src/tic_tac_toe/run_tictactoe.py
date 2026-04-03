"""CLI runner for the Tic-Tac-Toe portion of Project 4."""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from .game import Move, TicTacToeState
from .minimax import AlphaBetaAgent, MinimaxAgent
from .opponents import build_opponent

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"


def _move_to_json(move: Move | None) -> list[int] | None:
    return None if move is None else [move[0], move[1]]


def play_game(*, instance: str, config: str = "minimax", seed: int | None = None) -> dict[str, object]:
    rng = random.Random(seed)
    state = TicTacToeState()
    agent = build_agent(config)
    opponent = build_opponent(instance, rng=rng)

    trace: list[dict[str, object]] = []
    moves_taken = 0
    total_nodes = 0

    started = time.perf_counter()
    while not state.is_terminal():
        if state.player == agent.symbol:
            result = agent.choose_move(state)
            move = result.move
            total_nodes += result.nodes_evaluated
            actor = config
        else:
            move = opponent.choose_move(state)
            result = None
            actor = instance

        if move is None:
            raise ValueError("A non-terminal state must always produce a move.")

        state = state.apply_move(move)
        moves_taken += 1

        trace.append(
            {
                "step": len(trace),
                "actor": actor,
                "player": "X" if actor == config else "O",
                "move": _move_to_json(move),
                "board": state.to_trace_board(),
                "nodes_evaluated": None if result is None else result.nodes_evaluated,
                "score": None if result is None else result.score,
            }
        )

    runtime_ms = round((time.perf_counter() - started) * 1000, 3)

    return {
        "problem": "tictactoe",
        "instance": instance,
        "config": config,
        "result": state.result_label(maximizing_player=agent.symbol),
        "runtime_ms": runtime_ms,
        "nodes_evaluated": total_nodes,
        "moves_taken": moves_taken,
        "trace": trace,
        "winner": state.winner(),
        "final_board": state.to_trace_board(),
    }


def build_agent(config: str):
    if config == "minimax":
        return MinimaxAgent(symbol="X")
    if config == "alphabeta":
        return AlphaBetaAgent(symbol="X")
    raise ValueError("Tic-Tac-Toe config must be 'minimax' or 'alphabeta'.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Project 4 Tic-Tac-Toe agent.")
    parser.add_argument("--problem", default="tictactoe", choices=["tictactoe"])
    parser.add_argument("--instance", required=True, choices=["random", "scripted"])
    parser.add_argument("--config", default="minimax", choices=["minimax", "alphabeta"])
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--games",
        type=int,
        default=1,
        help="Number of games to run. Results are printed and also saved as JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output file path for a single-game run.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    results = [
        play_game(
            instance=args.instance,
            config=args.config,
            seed=None if args.seed is None else args.seed + game_number,
        )
        for game_number in range(args.games)
    ]

    DEFAULT_RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.games == 1:
        output_path = args.output or DEFAULT_RESULTS_DIR / f"tictactoe_{args.instance}_{args.config}.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(results[0], indent=2), encoding="utf-8")
        print(json.dumps({**results[0], "output_file": str(output_path)}, indent=2))
        return

    summary = {
        "problem": "tictactoe",
        "instance": args.instance,
        "config": args.config,
        "games": args.games,
        "wins": sum(1 for result in results if result["result"] == "win"),
        "draws": sum(1 for result in results if result["result"] == "draw"),
        "losses": sum(1 for result in results if result["result"] == "loss"),
        "avg_runtime_ms": round(sum(result["runtime_ms"] for result in results) / args.games, 3),
        "avg_nodes_evaluated": round(
            sum(result["nodes_evaluated"] for result in results) / args.games, 3
        ),
        "results": results,
    }
    output_path = DEFAULT_RESULTS_DIR / f"tictactoe_{args.instance}_{args.config}_{args.games}games.json"
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({**summary, "output_file": str(output_path)}, indent=2))


if __name__ == "__main__":
    main()
