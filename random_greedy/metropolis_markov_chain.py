import numpy as np
import sys
from board import Board
from read_board import read_board
from random_greedy import random_greedy
import timeit

def metropolis_RLS(board, _lambda):
    N = board.N
    while board.marked_cells < N**2:
        cell = board.choose_random_cell()
        symbol = board[cell].choose_random_symbol()
        if symbol == 0:
            if board[cell].symbol > 0:
                p = 1 / _lambda
                update = np.random.choice([0, 1], 1, p=[1 - p, p])
                if update == 1:
                    board.fix_board_remove_symbol(cell)
        else:
            if board[cell].symbol > 0:
              board.fix_board_change_symbol(cell, symbol)
            else:
                #board.fix_board_add_symbol(cell, symbol, random_greedy=False)
                board.fix_board_add_symbol(cell, symbol, random_greedy=False)


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

board.start_time = timeit.default_timer()
metropolis_RLS(board, _lambda)

