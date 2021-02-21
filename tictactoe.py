"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    sum_of_values = 0
    for row in board:
        for val in row:
            if val == X:
                sum_of_values += 1
            elif val == O:
                sum_of_values += -1
    if sum_of_values == 1:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError

    current_player = player(board)
    #print(type(action))
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    wins = [[(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]]

    for combination in wins:
        checks_x = 0
        checks_o = 0
        for i, j in combination:
            if board[i][j] == X:
                checks_x += 1
            if board[i][j] == O:
                checks_o += 1
        if checks_x == 3:
            return X
        if checks_o == 3:
            return O

    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or not actions(board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_player = winner(board)
    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else :
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    best_action = (0, 1)
    # Optimization by hardcoding the first move
    if board == initial_state():
        return best_action

    current_player = player(board)
    if current_player == X:
        best_value = float("-inf")
    else:
        best_value = float("inf")

    for action in actions(board):
        new_value = minimax_value(result(board, action), best_value)

        if current_player == X:
            new_value = max(best_value, new_value)

        if current_player == O:
            new_value = min(best_value, new_value)

        if new_value != best_value:
            best_value = new_value
            best_action = action

    return best_action


def minimax_value(board, best_value):
    """
    Returns the best value for each recursive minimax iteration.
    If the new value found is better thann the best value 
    then return without checking the others.
    Works by knowing the winning action for X is one that forces O to make a non-winning action
    Agent will look ahead in time at all the consequences and rewards if it were to make the action it considers
    It will then choose the action that has the most reward for it, in that it forces O to not have reward at all
    """
    if terminal(board):
        return utility(board)

    current_player = player(board)
    if current_player == X:
        value = float("-inf")
    else:
        value = float("inf")

    for action in actions(board):
        new_value = minimax_value(result(board, action), value)

        if current_player == X:
            if new_value > best_value:
                return new_value
            value = max(value, new_value)

        if current_player == O:
            if new_value < best_value:
                return new_value
            value = min(value, new_value)

    return value



