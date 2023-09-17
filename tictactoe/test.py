from tictactoe import initial_state, player, actions, result, winner, terminal, utility, minimax, max_value, min_value
import copy



board = initial_state()

_actions = actions(board)
print(_actions)
for action in _actions:
    print(max_value(board))

