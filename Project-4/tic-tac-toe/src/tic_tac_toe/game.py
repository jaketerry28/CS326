"""Core Tic-Tac-Toe game state and rules."""

from __future__ import annotations

from dataclasses import dataclass

Move = tuple[int, int]
Board = tuple[str, ...]
WIN_LINES: tuple[tuple[int, int, int], ...] = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def move_to_index(move: Move) -> int:
    row, col = move
    return row * 3 + col


def index_to_move(index: int) -> Move:
    return divmod(index, 3)


@dataclass(frozen=True, slots=True)
class TicTacToeState:
    """Immutable 3x3 Tic-Tac-Toe state."""

    board: Board = (" ",) * 9
    player: str = "X"

    def legal_moves(self) -> list[Move]:
        return [index_to_move(index) for index, cell in enumerate(self.board) if cell == " "]

    def apply_move(self, move: Move) -> "TicTacToeState":
        index = move_to_index(move)
        if self.board[index] != " ":
            raise ValueError(f"Move {move} is not legal.")

        next_board = list(self.board)
        next_board[index] = self.player
        next_player = "O" if self.player == "X" else "X"
        return TicTacToeState(board=tuple(next_board), player=next_player)

    def winner(self) -> str | None:
        for a, b, c in WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_terminal(self) -> bool:
        return self.winner() is not None or all(cell != " " for cell in self.board)

    def utility(self, maximizing_player: str = "X") -> int:
        winner = self.winner()
        if winner is None:
            return 0
        if winner == maximizing_player:
            return 1
        return -1

    def result_label(self, maximizing_player: str = "X") -> str:
        score = self.utility(maximizing_player)
        if score > 0:
            return "win"
        if score < 0:
            return "loss"
        return "draw"

    def board_rows(self) -> list[list[str]]:
        return [list(self.board[row * 3 : row * 3 + 3]) for row in range(3)]

    def to_trace_board(self) -> list[list[str]]:
        return self.board_rows()
