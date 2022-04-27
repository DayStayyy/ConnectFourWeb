import numpy as np
import math
import random
from random import randint
def winning_move(board, piece,COLUMN_COUNT,ROW_COUNT):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
#======================


def evaluate_window(window, piece,COLUMN_COUNT,ROW_COUNT,PLAYER_PIECE,AI_PIECE,EMPTY=0):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH,PLAYER_PIECE,AI_PIECE):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece,COLUMN_COUNT,ROW_COUNT,PLAYER_PIECE,AI_PIECE)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece,COLUMN_COUNT,ROW_COUNT,PLAYER_PIECE,AI_PIECE)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece,COLUMN_COUNT,ROW_COUNT,PLAYER_PIECE,AI_PIECE)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece,COLUMN_COUNT,ROW_COUNT,PLAYER_PIECE,AI_PIECE)

    return score

def is_terminal_node(board,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT):
    return winning_move(board, PLAYER_PIECE,COLUMN_COUNT,ROW_COUNT) or winning_move(board, AI_PIECE,COLUMN_COUNT,ROW_COUNT) or len(get_valid_locations(board,COLUMN_COUNT,ROW_COUNT)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH):
    valid_locations = get_valid_locations(board,COLUMN_COUNT,ROW_COUNT)
    is_terminal = is_terminal_node(board,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE,COLUMN_COUNT,ROW_COUNT):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE,COLUMN_COUNT,ROW_COUNT):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH,PLAYER_PIECE,AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col,ROW_COUNT)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col,ROW_COUNT)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board,COLUMN_COUNT,ROW_COUNT):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col,ROW_COUNT):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH,PLAYER_PIECE,AI_PIECE):

    valid_locations = get_valid_locations(board,COLUMN_COUNT,ROW_COUNT)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH,PLAYER_PIECE,AI_PIECE)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col,ROW_COUNT):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col,ROW_COUNT):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def create_board(ROW_COUNT,COLUMN_COUNT):
    return np.zeros((ROW_COUNT,COLUMN_COUNT))

def apiConnectFour(BoardStr,level=2) :
    AI_PIECE = 1
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    PLAYER_PIECE = 1
    AI_PIECE = 2
    WINDOW_LENGTH = 4

    if(len(BoardStr) != 42) :
        return -1
    board = create_board(6,7)
    loop = 0
    for i in range(6) :
        for j in range(7) :
            if BoardStr[loop] != "0" :
                board[i][j] = int(BoardStr[loop])
            loop += 1

    if level == "1" :
        return randomApi(board)
    elif level == "2" :
        return minMaxApi(board,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH)
    return -1


def randomApi(board) :
    result = randint(1,7)
    while(len(board[result]) == 6) :
        result = randint(1,8)
    return result

def minMaxApi(board,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH) :
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True,PLAYER_PIECE,AI_PIECE,COLUMN_COUNT,ROW_COUNT,WINDOW_LENGTH)
    if is_valid_location(board, col,ROW_COUNT):
        return col

# print(apiConnectFour("001000000000000000000000000000000000000000"))

#000000000000000000000000000000000000000000