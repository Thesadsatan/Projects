# Tic-Tac-Toe

The program plays Tic-Tac-Toe optimally as AI using __Minimax Algorithm__ built by using __PyGame__.

![image](https://github.com/Thesadsatan/projects/assets/99989899/b821580e-e853-432a-8beb-f83020e63b14)


# Overview
The Game has several functions as follows that enable the program to play the game optimally.
## player

The player function takes a board state as input, and returns which player’s turn it is (either X or O).
* In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move.
## actions

The actions function returns a set of all of the possible actions that can be taken on a given board.
* Each action is represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2) and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
* Possible moves are any cells on the board that do not already have an X or an O in them.
## result 

The result function takes a board and an action as input, and returns a new board state, without modifying the original board.
If action is not a valid action for the board, the program raises an exception.
The returned board state is the board that would result from taking the original input board, and letting the player whose turn it is make their move at the cell indicated by the input action.
Importantly, the original board is left unmodified: since Minimax will ultimately require considering many different board states during its computation. This leads the program to make a deep copy of the board first before making any changes.
## winner

The winner function accepts a board as input, and returns the winner of the board if there is one.
If the X player has won the game, the function returns X. If the O player has won the game, the function returns O.
One can win the game with three of their moves in a row horizontally, vertically, or diagonally.
* If there is no winner of the game (either because the game is in progress, or because it ended in a tie), the function returns None.
## terminal

The terminal function accepts a board as input, and returns a boolean value indicating whether the game is over.
If the game is over, either because someone has won the game or because all cells have been filled without anyone winning, the function returns True.
Otherwise, the function returns False if the game is still in progress.
## utility

The utility function accepts a terminal board as input and output the utility of the board.
If X has won the game, the utility is 1. If O has won the game, the utility is -1. If the game has ended in a tie, the utility is 0.
## minimax.

The minimax function takes a board as input, and returns the optimal move for the player to move on that board.
* The move returned is the optimal action (i, j) that is one of the allowable actions on the board. If multiple moves are equally optimal, the program returns any of those moves.
* If the board is a terminal board, the minimax function returns None.
