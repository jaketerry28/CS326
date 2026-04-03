from tic_tac_toe.game import TicTacToeState
from tic_tac_toe.minimax import AlphaBetaAgent, MinimaxAgent


def test_legal_moves_generated_correctly():
    state = TicTacToeState(
        board=(
            "X", "O", "X",
            " ", "O", " ",
            " ", "X", " ",
        ),
        player="O",
    )

    assert state.legal_moves() == [(1, 0), (1, 2), (2, 0), (2, 2)]


def test_terminal_states_recognized_correctly():
    x_wins = TicTacToeState(
        board=(
            "X", "X", "X",
            "O", "O", " ",
            " ", " ", " ",
        ),
        player="O",
    )
    draw = TicTacToeState(
        board=(
            "X", "O", "X",
            "X", "O", "O",
            "O", "X", "X",
        ),
        player="X",
    )

    assert x_wins.is_terminal() is True
    assert x_wins.winner() == "X"
    assert x_wins.utility("X") == 1

    assert draw.is_terminal() is True
    assert draw.winner() is None
    assert draw.utility("X") == 0


def test_minimax_chooses_utility_maximizing_move():
    state = TicTacToeState(
        board=(
            "X", "X", " ",
            "O", "O", " ",
            " ", " ", " ",
        ),
        player="X",
    )
    agent = MinimaxAgent(symbol="X")

    result = agent.choose_move(state)

    assert result.move == (0, 2)
    assert result.score == 1
    assert result.nodes_evaluated > 0


def test_minimax_prefers_immediate_win_when_multiple_wins_exist():
    state = TicTacToeState(
        board=(
            "X", "O", "O",
            "X", " ", " ",
            " ", " ", " ",
        ),
        player="X",
    )
    agent = MinimaxAgent(symbol="X")

    result = agent.choose_move(state)

    assert result.move == (2, 0)
    assert result.score == 1


def test_alphabeta_matches_minimax_and_evaluates_no_more_nodes():
    state = TicTacToeState(
        board=(
            "X", " ", " ",
            " ", "O", " ",
            " ", " ", "X",
        ),
        player="O",
    )
    minimax = MinimaxAgent(symbol="O")
    alphabeta = AlphaBetaAgent(symbol="O")

    minimax_result = minimax.choose_move(state)
    alphabeta_result = alphabeta.choose_move(state)

    assert alphabeta_result.move == minimax_result.move
    assert alphabeta_result.score == minimax_result.score
    assert alphabeta_result.nodes_evaluated <= minimax_result.nodes_evaluated
