import numpy as np
from random import randint

from regex import B

def create_board(ROW_COUNT,COLUMN_COUNT):
    return np.zeros((ROW_COUNT,COLUMN_COUNT))


def randomApi(BoardStr) :
    if(len(BoardStr) != 42) :
        return -1
    board = create_board(6,7)
    result = randint(1,8)
    while(len(board[result]) == 6) :
        result = randint(1,8)
    return result