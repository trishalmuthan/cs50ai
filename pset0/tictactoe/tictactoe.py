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
    count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X or board[row][col] == O:
                count += 1

    if count % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    toReturn = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != X and board[row][col] != O:
                toReturn.add((row, col))

    return toReturn


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid Action")
    newBoard = copy.deepcopy(board)
    current = player(board)

    newBoard[action[0]][action[1]] = current
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2]:
            if board[row][0] == X:
                return X
            elif board[row][0] == O:
                return O
            else:
                return None
    
    # check cols
    for col in range(len(board[0])):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == X:
                return X
            elif board[0][col] == O:
                return O
            else:
                return None

     # Check diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
        else:
            return None

    # Check diagonal
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return X
        elif board[0][2] == O:
            return O
        else:
            return None

    # else
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == EMPTY:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]

def max_value(board):
    if terminal(board):
        return [utility(board), None]

    move = None
    v = float('-inf')
    store = v
    for action in actions(board):
        store = v
        v = max(v, min_value(result(board, action))[0])
        if v > store:
            store = v
            move = action
    return [v, move]

def min_value(board):
    if terminal(board):
        return [utility(board), None]
    move = None
    v = float('inf')
    store = v
    for action in actions(board):
        store = v
        v = min(v, max_value(result(board, action))[0])
        if v < store:
            store = v
            move = action
    
    return [v, move]

    
