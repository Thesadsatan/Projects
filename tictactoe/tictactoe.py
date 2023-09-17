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
    # initialze 2 variables to keep track of the number of moves each X and O made as I loop through the board
    x_counter = 0
    o_counter = 0

    # loop through each row in the board
    for row in board:
        # loop through each cell in the row 
        for cell in row:
            # check the stae of the cell and update the corresponding variable
            if cell == X:
                x_counter +=1
            
            if cell == O:
                o_counter +=1
    
    # check whose turn it is and return the Player
    if x_counter <= o_counter:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # initialize a set which eventually contains all the possible acctions
    possible_actions = set()

    # loop through each row
    for i, row in enumerate(board):
        # loop through each cell in the row
        for j, cell in enumerate(row):
            # update the possible actions if the cell is EMPTY
            if not cell:
                action = (i, j)
                possible_actions.add(action)

    # return the set of all possible actions
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # make a copy of the board
    board_copy = copy.deepcopy(board)

    # get the i and j from action
    i = action[0]
    j = action[1]
    
    # check who's taking the action
    _player = player(board_copy)

    # check whether the action is allowed
    try:
        board_copy[i][j] = _player
        return board_copy
    except IndexError:
        raise IndexError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2]:
        return board[0][0]

    if board[1][0] == board[1][1] == board[1][2]:
        return board[1][0] 
    
    if board[2][0] == board[2][1] == board[2][2]:
        return board[2][0]

    if board[0][0] == board[1][0] == board[2][0]:
        return board[0][0]    

    if board[0][1] == board[1][1] == board[2][1]:
        return board[0][1] 

    if board[0][2] == board[1][2] == board[2][2]:
        return board[0][2] 
    
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0] 
    
    if board[2][0] == board[1][1] == board[0][2]:
        return board[2][0] 

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check whether the game is terminated by a win
    if winner(board):
        return True
    
    # loop through each row
    for row in board:

        # loop through each cell
        for cell in row:

            # check if the cell is EMPTY and return False
            if not cell:
                return False
    
    # return True if all cells have been filled
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # return 1 if X won
    if winner(board) == X:
        return 1
    
    # return 1 if O won
    if winner(board) == O:
        return -1
    
    # return 0 if no winner
    return 0


def max_value(board, min_v):

    # initialize V to negative infinity
    v = -math.inf

    # check if the board is a terminal board
    if terminal(board):
        return utility(board)

    # get all the possible actions for the current state
    _actions = actions(board)
    
    for action in _actions:
        v = max(v, min_value(result(board, action), v))
        if v > min_v:
            return v
    return v


def min_value(board, max_v):
  
    # initialize V to negative infinity
    v = math.inf

    # check if the board is a terminal board
    if terminal(board):
        return utility(board)

    # get all the possible actions for the current state
    _actions = actions(board)
    
    for action in _actions:
        v = min(v, max_value(result(board, action), v))
        if v < max_v:
            return v

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # check if the board is a terminal board
    if terminal(board):
        return None
    
    # check all the possible actions
    _actions = actions(board)
    
    # check whose turn it is 
    _player = player(board)

    v = 0

    if _player == X:     
        v = -math.inf

    if _player == O:
         v = math.inf
    
    optimal_move = None

    # find the optimal action
    for action in _actions:

        if _player == X:
            _min_value = min_value(result(board,action), v)
            if v < _min_value:
                v = _min_value
                optimal_move = action

        if _player == O:
            _max_value = max_value(result(board,action), v)
            if v > _max_value:
                v = _max_value
                optimal_move = action 

    return optimal_move



