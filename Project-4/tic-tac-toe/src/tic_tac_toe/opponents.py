"""Configurable opponents for the Tic-Tac-Toe runner."""

from __future__ import annotations

import random

from .game import Move, TicTacToeState


class RandomOpponent:
    """Opponent that chooses uniformly among legal moves."""

    def __init__(self, symbol: str = "O", rng: random.Random | None = None) -> None:
        self.symbol = symbol
        self.rng = rng or random.Random()

    def choose_move(self, state: TicTacToeState) -> Move:
        if state.player != self.symbol:
            raise ValueError("Random opponent can only move on its own turn.")
        return self.rng.choice(state.legal_moves())


class ScriptedOpponent:
    """Deterministic opponent with a fixed move preference order."""

    def __init__(self, symbol: str = "O") -> None:
        self.symbol = symbol
        self.priority: list[Move] = [
            (1, 1),
            (0, 0),
            (0, 2),
            (2, 0),
            (2, 2),
            (0, 1),
            (1, 0),
            (1, 2),
            (2, 1),
        ]

    def choose_move(self, state: TicTacToeState) -> Move:
        if state.player != self.symbol:
            raise ValueError("Scripted opponent can only move on its own turn.")
        legal = set(state.legal_moves())
        for move in self.priority:
            if move in legal:
                return move
        raise ValueError("No legal moves remain for scripted opponent.")


def build_opponent(instance: str, *, rng: random.Random | None = None):
    if instance == "random":
        return RandomOpponent(rng=rng)
    if instance == "scripted":
        return ScriptedOpponent()
    raise ValueError("Instance must be 'random' or 'scripted'.")
