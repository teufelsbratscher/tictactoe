import sys
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    if board == initial_state():
        return X
    flat_board = [cell for row in board for cell in row]
    num_x = flat_board.count('X')
    num_o = flat_board.count('O')
    if num_x > num_o:
        return O
    return X

"""
actions() function is not working properly. I ran it and checked what it returns. I passed a board with just one
empty position (1,1) and the function returned this {((1,), (1,))} instead of {(1,1)}. This is causing the 
>> IndexError: tuple index out of range
That's why it is important to test all your funcions separately. That way you would immidiately notice the error
The code on Line 39 is causing the problem. The zip() on Line 33 doesn't work like you might expect. You can get rid of 
that line altogehter. Then just slightly modify Line 40. Add the tuple directly to possible_actions (without using zip(). 
"""
def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available_cell = tuple(zip((i, j)))
                possible_actions.add(available_cell)
    return possible_actions


"""
Although your result() function works properly it would be more optimal to create a copy_of_board after you checked that 
the action is valid. In case where the action is invalid there is no need to create a copy of the board. You save some
memory that way. In this particular project it doesn't matter so much but it is good to know for the future. Also your
if statement could be simpler if you check if the board[i][j] is not empty instead of checking for both X and O.
"""
def result(board, action):
    copy_of_board = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    if board[i][j] == X or board[i][j] == O:
        raise Exception("Invalid action.")
    copy_of_board[i][j] = player(board)
    return copy_of_board


def winner(board):
    if board[0].count(X) == 3:
        return X
    if board[1].count(X) == 3:
        return X
    if board[2].count(X) == 3:
        return X

    if board[0].count(O) == 3:
        return O
    if board[1].count(O) == 3:
        return O
    if board[2].count(O) == 3:
        return O

    if board[0][0] == board[1][0] == board[2][0] == X:
        return X
    if board[0][1] == board[1][1] == board[2][1] == X:
        return X
    if board[0][2] == board[1][2] == board[2][2] == X:
        return X

    if board[0][0] == board[1][0] == board[2][0] == O:
        return O
    if board[0][1] == board[1][1] == board[2][1] == O:
        return O
    if board[0][2] == board[1][2] == board[2][2] == O:
        return O

    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    if board[0][2] == board[1][1] == board[2][0] == X:
        return X

    if board[0][0] == board[1][1] == board[2][2] == O:
        return O
    if board[0][2] == board[1][1] == board[2][0] == O:
        return O

    else:
        return None


"""
There is an error here as well. The board is a list of lists so your for loop on line 114 does not check every cell.
You have to nest in one more for loop. So you iterate through every row in the board and then every cell in the row.
In general there is a much shorter way to code this function, especially the part where you check if all cells are 
either X or O. But it works fine. When you're finished with your project you can check my code on github.
"""
def terminal(board):
    if winner(board) == X or winner(board) == O:
        return True

    if winner(board) != X and winner(board) != O:
        for cell in board:
            if cell == EMPTY:
                return False

    num_row1 = board[0].count('X') + board[0].count('O')
    num_row2 = board[1].count('X') + board[1].count('O')
    num_row3 = board[2].count('X') + board[2].count('O')
    if num_row1 + num_row2 + num_row3 == 9:
        return True


"""
this works fine, but it's not necessery to check if board is in terminal state because the utility func is anyway only
called if termianl state is true. Look at line 141-142 and 149-150.
"""
def utility(board):
    if terminal(board):
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -sys.maxsize
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = sys.maxsize
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
"""
You have to check if the board is in terminal state before you check if it's X or O move. If the game is over 
there is no need to look for optimal move. Also if the game is over minimax() should return None, not the utility().
Only min_value and max_value return the utility(). The way you have it above is correct.
So the main function flow should be:
if game over -> return None; elif X's move -> look for X's best move; elif O's move -> look for O's best move
Also every player needs his own for loop looping through all available actions (like the way you had it on the discussion
board on ED) so the your code on line 164 is in the wrong place.
"""
    for action in actions(board):
        if player(board) == X:
            if terminal(board):
                return utility(board)
            x_val = -1
            x_val = max(min_value(action), x_val)
            return x_val

        if player(board) == O:
            if terminal(board):
                return utility(board)
            o_val = 1
            o_val = min(max_value(action), o_val)
            return o_val
