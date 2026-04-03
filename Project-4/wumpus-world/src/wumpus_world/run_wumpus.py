"""CLI runner for the Wumpus World baseline configuration."""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

from .agent import KnowledgeBasedWumpusAgent
from .environment import WumpusWorld
from .layouts import WUMPUS_LAYOUTS, get_layout

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RESULTS_DIR = PROJECT_ROOT / "results"


def run_wumpus_instance(
    *,
    instance: str,
    config: str = "kb",
    seed: int | None = None,
) -> dict[str, object]:
    if config != "kb":
        raise ValueError("The only supported Wumpus configuration right now is 'kb'.")

    if seed is not None:
        random.seed(seed)

    layout = get_layout(instance)
    world = WumpusWorld(layout)
    agent = KnowledgeBasedWumpusAgent(world)

    started = time.perf_counter()
    agent_result = agent.run()
    runtime_ms = round((time.perf_counter() - started) * 1000, 3)

    return {
        "problem": "wumpus",
        "instance": instance,
        "config": config,
        "success": agent_result["success"],
        "runtime_ms": runtime_ms,
        "states_expanded": agent_result["states_expanded"],
        "moves_taken": agent_result["moves_taken"],
        "trace": agent_result["trace"],
        "layout_description": layout.description,
        "visited_squares": agent_result["visited_squares"],
        "total_safe_squares": agent_result["total_safe_squares"],
        "fully_explored": agent_result["fully_explored"],
        "failure_reason": agent_result["failure_reason"],
        "knowledge_summary": agent_result["knowledge_summary"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Project 4 Wumpus World agent.")
    parser.add_argument("--problem", default="wumpus", choices=["wumpus"])
    parser.add_argument("--instance", required=True, choices=sorted(WUMPUS_LAYOUTS))
    parser.add_argument("--config", default="kb", choices=["kb"])
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path for the JSON result file.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_wumpus_instance(instance=args.instance, config=args.config, seed=args.seed)

    output_path = args.output
    if output_path is None:
        DEFAULT_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        output_path = DEFAULT_RESULTS_DIR / f"wumpus_{args.instance}_{args.config}.json"
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    saved_result = {**result, "output_file": str(output_path)}
    output_path.write_text(json.dumps(saved_result, indent=2), encoding="utf-8")
    print(json.dumps(saved_result, indent=2))


if __name__ == "__main__":
    main()
