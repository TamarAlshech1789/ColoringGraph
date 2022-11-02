import numpy as np
import sys
import random
from board import Board
from read_board import read_board
from random_greedy import random_greedy


def CellAndSymbol_AddZero_metropolis_RLS(board, _lambda):
    N = board.N
    p = 1 / _lambda
    while board.marked_cells < N **2:
        (cell, symbol) = board.choose_good_random_cell_and_symbol()

        if symbol == 0:
            choice = np.random.choice([0, 1], 1, p=[1 - p, p])
            if choice[0] == 1:
                board.fix_board_remove_symbol(cell)
        else:
            if board[cell].symbol == 0:
                board.fix_board_add_symbol(cell, symbol)
            else:
                board.fix_board_change_symbol(cell, symbol)


        """
        choice = np.random.choice([0, 1], 1, p=[1 - p, p])
        if choice[0] == 1:
            (cell, symbol) = random.choice(board.zero_cells)
        else:
            (cell, symbol) = board.choose_good_random_cell_and_symbol()
            if cell == (-1,-1):
                (cell, symbol) = random.choice(board.zero_cells)

        if symbol == 0:
            board.fix_board_remove_symbol(cell)
        elif board[cell].symbol == 0:
            board.fix_board_add_symbol(cell, symbol, random_greedy=False)
        else:
            board.fix_board_change_symbol(cell, symbol)
        """

#input params are:
# N     lambda      is_cluster      read_board
N = int(sys.argv[1])
_lambda = float(sys.argv[2])
#_lambda = N ** 2
#is_cluster = sys.argv[3] == '1'
is_cluster = True
#_read_board = sys.argv[4] == '1'
_read_board = False

if _read_board:
    board = Board(N=N, is_cluster=is_cluster, _lambda=_lambda)
    read_board(board)
else:
    board = random_greedy(N=N, is_cluster=is_cluster, _lambda=_lambda)

CellAndSymbol_AddZero_metropolis_RLS(board, _lambda)

