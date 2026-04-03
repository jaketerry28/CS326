"""Generate report plots from Project 4 JSON outputs."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
PLOTS_DIR = PROJECT_ROOT / "plots"
WUMPUS_RESULTS = PROJECT_ROOT / "wumpus-world" / "results"
TICTACTOE_RESULTS = PROJECT_ROOT / "tic-tac-toe" / "results"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_wumpus_rows() -> pd.DataFrame:
    rows = []
    for path in sorted(WUMPUS_RESULTS.glob("wumpus_*_kb.json")):
        data = load_json(path)
        visited = data["visited_squares"]
        total_safe = data["total_safe_squares"]
        rows.append(
            {
                "instance": data["instance"],
                "success": int(data["success"]),
                "runtime_ms": data["runtime_ms"],
                "states_expanded": data["states_expanded"],
                "moves_taken": data["moves_taken"],
                "visited_safe_pct": 100.0 * visited / total_safe,
                "visited_label": f"{visited}/{total_safe}",
            }
        )
    return pd.DataFrame(rows)


def load_tictactoe_rows() -> pd.DataFrame:
    rows = []
    for path in sorted(TICTACTOE_RESULTS.glob("tictactoe_*_*_*games.json")):
        data = load_json(path)
        rows.append(
            {
                "instance": data["instance"],
                "config": data["config"],
                "games": data["games"],
                "wins": data["wins"],
                "draws": data["draws"],
                "losses": data["losses"],
                "avg_runtime_ms": data["avg_runtime_ms"],
                "avg_nodes_evaluated": data["avg_nodes_evaluated"],
            }
        )
    return pd.DataFrame(rows)


def plot_wumpus(df: pd.DataFrame) -> None:
    df = df.set_index("instance").loc[["easy_1", "easy_2", "hard_1", "hard_2"]].reset_index()

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    colors = ["#2f855a" if success else "#c05621" for success in df["success"]]
    axes[0].bar(df["instance"], df["visited_safe_pct"], color=colors)
    axes[0].set_title("Wumpus Safe-Square Coverage")
    axes[0].set_ylabel("Visited Safe Squares (%)")
    axes[0].set_ylim(0, 110)
    for idx, label in enumerate(df["visited_label"]):
        axes[0].text(idx, df.loc[idx, "visited_safe_pct"] + 2, label, ha="center", fontsize=9)

    axes[1].bar(df["instance"], df["moves_taken"], color="#2b6cb0")
    axes[1].set_title("Wumpus Moves Taken by Layout")
    axes[1].set_ylabel("Moves Taken")
    for idx, moves in enumerate(df["moves_taken"]):
        axes[1].text(idx, moves + 0.3, str(moves), ha="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "wumpus_layout_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_tictactoe_runtime(df: pd.DataFrame) -> None:
    ordered = df.sort_values(["instance", "config"]).copy()
    instances = ["random", "scripted"]
    configs = ["minimax", "alphabeta"]
    x = range(len(instances))
    width = 0.35

    runtime_lookup = {
        (row["instance"], row["config"]): row["avg_runtime_ms"]
        for _, row in ordered.iterrows()
    }
    nodes_lookup = {
        (row["instance"], row["config"]): row["avg_nodes_evaluated"]
        for _, row in ordered.iterrows()
    }

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    minimax_runtime = [runtime_lookup[(instance, "minimax")] for instance in instances]
    alphabeta_runtime = [runtime_lookup[(instance, "alphabeta")] for instance in instances]
    axes[0].bar([idx - width / 2 for idx in x], minimax_runtime, width=width, label="minimax", color="#805ad5")
    axes[0].bar([idx + width / 2 for idx in x], alphabeta_runtime, width=width, label="alphabeta", color="#dd6b20")
    axes[0].set_xticks(list(x), instances)
    axes[0].set_title("Tic-Tac-Toe Average Runtime")
    axes[0].set_ylabel("Runtime (ms)")
    axes[0].legend()

    minimax_nodes = [nodes_lookup[(instance, "minimax")] for instance in instances]
    alphabeta_nodes = [nodes_lookup[(instance, "alphabeta")] for instance in instances]
    axes[1].bar([idx - width / 2 for idx in x], minimax_nodes, width=width, label="minimax", color="#805ad5")
    axes[1].bar([idx + width / 2 for idx in x], alphabeta_nodes, width=width, label="alphabeta", color="#dd6b20")
    axes[1].set_xticks(list(x), instances)
    axes[1].set_title("Tic-Tac-Toe Average Nodes Evaluated")
    axes[1].set_ylabel("Nodes Evaluated")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "tictactoe_search_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_tictactoe_outcomes(df: pd.DataFrame) -> None:
    ordered = df.sort_values(["instance", "config"]).copy()
    labels = [f"{row['instance']}\n{row['config']}" for _, row in ordered.iterrows()]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    wins = ordered["wins"].tolist()
    draws = ordered["draws"].tolist()
    losses = ordered["losses"].tolist()

    ax.bar(labels, wins, label="wins", color="#2f855a")
    ax.bar(labels, draws, bottom=wins, label="draws", color="#d69e2e")
    ax.bar(
        labels,
        losses,
        bottom=[wins[i] + draws[i] for i in range(len(wins))],
        label="losses",
        color="#c53030",
    )
    ax.set_title("Tic-Tac-Toe Outcomes by Opponent and Search")
    ax.set_ylabel("Games")
    ax.legend()

    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "tictactoe_outcomes.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def plot_tictactoe_random_10game_bars() -> None:
    minimax_path = TICTACTOE_RESULTS / "tictactoe_random_minimax_10games.json"
    alphabeta_path = TICTACTOE_RESULTS / "tictactoe_random_alphabeta_10games.json"

    minimax_data = load_json(minimax_path)["results"]
    alphabeta_data = load_json(alphabeta_path)["results"]

    game_numbers = list(range(1, len(minimax_data) + 1))
    minimax_runtime = [game["runtime_ms"] for game in minimax_data]
    alphabeta_runtime = [game["runtime_ms"] for game in alphabeta_data]
    minimax_nodes = [game["nodes_evaluated"] for game in minimax_data]
    alphabeta_nodes = [game["nodes_evaluated"] for game in alphabeta_data]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    width = 0.38
    positions = list(range(len(game_numbers)))

    axes[0].bar(
        [position - width / 2 for position in positions],
        minimax_runtime,
        width=width,
        color="#805ad5",
        label="minimax",
    )
    axes[0].bar(
        [position + width / 2 for position in positions],
        alphabeta_runtime,
        width=width,
        color="#dd6b20",
        label="alphabeta",
    )
    axes[0].set_title("Random Opponent Runtime by Game")
    axes[0].set_xlabel("Game Number")
    axes[0].set_ylabel("Runtime (ms)")
    axes[0].set_xticks(positions, game_numbers)
    axes[0].grid(True, axis="y", alpha=0.25)
    axes[0].legend()

    axes[1].bar(
        [position - width / 2 for position in positions],
        minimax_nodes,
        width=width,
        color="#805ad5",
        label="minimax",
    )
    axes[1].bar(
        [position + width / 2 for position in positions],
        alphabeta_nodes,
        width=width,
        color="#dd6b20",
        label="alphabeta",
    )
    axes[1].set_title("Random Opponent Nodes Evaluated by Game")
    axes[1].set_xlabel("Game Number")
    axes[1].set_ylabel("Nodes Evaluated")
    axes[1].set_xticks(positions, game_numbers)
    axes[1].grid(True, axis="y", alpha=0.25)
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(PLOTS_DIR / "tictactoe_random_10games_bar_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    wumpus_df = load_wumpus_rows()
    tictactoe_df = load_tictactoe_rows()

    plot_wumpus(wumpus_df)
    plot_tictactoe_runtime(tictactoe_df)
    plot_tictactoe_outcomes(tictactoe_df)
    plot_tictactoe_random_10game_bars()

    print("Generated plots:")
    for path in sorted(PLOTS_DIR.glob("*.png")):
        print(path)


if __name__ == "__main__":
    main()
