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


def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available_cell = tuple(zip((i, j)))
                possible_actions.add(available_cell)
    return possible_actions


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



