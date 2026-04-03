"""Minimax and Alpha-Beta search agents for Tic-Tac-Toe."""

from __future__ import annotations

from dataclasses import dataclass

from .game import Move, TicTacToeState


def _prefer_shorter_win_or_longer_loss(
    *,
    score: int,
    candidate_plies: int,
    current_plies: int | None,
) -> bool:
    if current_plies is None:
        return True
    if score > 0:
        return candidate_plies < current_plies
    if score < 0:
        return candidate_plies > current_plies
    return candidate_plies < current_plies


@dataclass(frozen=True, slots=True)
class SearchResult:
    move: Move | None
    score: int
    nodes_evaluated: int
    plies_to_end: int


class MinimaxAgent:
    """Perfect-information agent using standard Minimax."""

    def __init__(self, symbol: str = "X") -> None:
        self.symbol = symbol

    def choose_move(self, state: TicTacToeState) -> SearchResult:
        if state.player != self.symbol:
            raise ValueError("Minimax agent can only move on its own turn.")
        return self._minimax(state)

    def _minimax(self, state: TicTacToeState) -> SearchResult:
        if state.is_terminal():
            return SearchResult(
                move=None,
                score=state.utility(self.symbol),
                nodes_evaluated=1,
                plies_to_end=0,
            )

        maximizing = state.player == self.symbol
        best_score = -2 if maximizing else 2
        best_move: Move | None = None
        nodes_evaluated = 1
        best_plies_to_end: int | None = None

        for move in state.legal_moves():
            child = state.apply_move(move)
            result = self._minimax(child)
            nodes_evaluated += result.nodes_evaluated
            candidate_plies = result.plies_to_end + 1

            if maximizing:
                if result.score > best_score or (
                    result.score == best_score
                    and _prefer_shorter_win_or_longer_loss(
                        score=result.score,
                        candidate_plies=candidate_plies,
                        current_plies=best_plies_to_end,
                    )
                ):
                    best_score = result.score
                    best_move = move
                    best_plies_to_end = candidate_plies
            else:
                if result.score < best_score or (
                    result.score == best_score
                    and _prefer_shorter_win_or_longer_loss(
                        score=result.score,
                        candidate_plies=candidate_plies,
                        current_plies=best_plies_to_end,
                    )
                ):
                    best_score = result.score
                    best_move = move
                    best_plies_to_end = candidate_plies

        return SearchResult(
            move=best_move,
            score=best_score,
            nodes_evaluated=nodes_evaluated,
            plies_to_end=0 if best_plies_to_end is None else best_plies_to_end,
        )


class AlphaBetaAgent:
    """Perfect-information agent using Minimax with Alpha-Beta pruning."""

    def __init__(self, symbol: str = "X") -> None:
        self.symbol = symbol

    def choose_move(self, state: TicTacToeState) -> SearchResult:
        if state.player != self.symbol:
            raise ValueError("Alpha-Beta agent can only move on its own turn.")
        return self._alphabeta(state, alpha=-2, beta=2)

    def _alphabeta(self, state: TicTacToeState, *, alpha: int, beta: int) -> SearchResult:
        if state.is_terminal():
            return SearchResult(
                move=None,
                score=state.utility(self.symbol),
                nodes_evaluated=1,
                plies_to_end=0,
            )

        maximizing = state.player == self.symbol
        best_score = -2 if maximizing else 2
        best_move: Move | None = None
        nodes_evaluated = 1
        best_plies_to_end: int | None = None

        for move in state.legal_moves():
            child = state.apply_move(move)
            result = self._alphabeta(child, alpha=alpha, beta=beta)
            nodes_evaluated += result.nodes_evaluated
            candidate_plies = result.plies_to_end + 1

            if maximizing:
                if result.score > best_score or (
                    result.score == best_score
                    and _prefer_shorter_win_or_longer_loss(
                        score=result.score,
                        candidate_plies=candidate_plies,
                        current_plies=best_plies_to_end,
                    )
                ):
                    best_score = result.score
                    best_move = move
                    best_plies_to_end = candidate_plies
                alpha = max(alpha, best_score)
            else:
                if result.score < best_score or (
                    result.score == best_score
                    and _prefer_shorter_win_or_longer_loss(
                        score=result.score,
                        candidate_plies=candidate_plies,
                        current_plies=best_plies_to_end,
                    )
                ):
                    best_score = result.score
                    best_move = move
                    best_plies_to_end = candidate_plies
                beta = min(beta, best_score)

            if alpha >= beta:
                break

        return SearchResult(
            move=best_move,
            score=best_score,
            nodes_evaluated=nodes_evaluated,
            plies_to_end=0 if best_plies_to_end is None else best_plies_to_end,
        )
