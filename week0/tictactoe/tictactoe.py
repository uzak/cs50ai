"""
Tic Tac Toe Player
"""

import copy


X = "X"
O = "O"
EMPTY = None

WINS = [
    [0, 1, 2], 
    [3, 4, 5], 
    [6, 7, 8], 
    [0, 4, 8], 
    [2, 4, 6], 
    [0, 3, 6], 
    [1, 4, 7], 
    [2, 5, 8],
]

def check_for_win(board, player, pos):
    a, b, c = pos
    return board[a] == player and \
        board[b] == player and \
        board[c] == player


def flatten_board(board):
    return [item for sublist in board for item in sublist]

def filter_board(board):
    return list(filter(lambda x: x is not None, flatten_board(board)))


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
    x = 0
    o = 0
    for row in board:
        for col in row:
            if col == X:
                x += 1
            elif col == O:
                o += 1
    result = X if (x == o or x == 0) else O
    #print(result, x, o)
    return result


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i, row in enumerate(board):
        for j, col in enumerate(board[i]):
            if board[i][j] is EMPTY:
                result.add((i, j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    board = copy.deepcopy(board)
    board[row][col] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    flattened = flatten_board(board)
    for player in [X, O]:
        for win_pos in WINS:
            if check_for_win(flattened, player, win_pos):
                return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(filter_board(board)) == len(WINS):
        return True
    
    if winner(board) is not None:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    #print("max_value", board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    #print("min_value", board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    p = player(board)
    action = None
    v = None
    for a in actions(board):
        next = result(board, a)
        if p == X:
            v = min_value(next)
            print(p, a, v)
            if v == 1:
                action = a
                break
        else:
            v = max_value(next)
            print(p, a, v)
            if v == -1:
                action = a
                break
        if v == 0:      # fallback
            action = a
    #print(p, board, action, v)
    return action