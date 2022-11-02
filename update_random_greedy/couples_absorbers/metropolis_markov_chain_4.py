import numpy as np
import sys
import copy
from board import Board
from read_board import read_board
from random_greedy import random_greedy


def CellAndSymbol_Absorbers_metropolis_RLS(board, _lambda):
    N = board.N
    board.MMC_empty_cells = copy.deepcopy(board.empty_cells)
    p = 1 / _lambda
    while board.marked_cells < N **2:
        update = np.random.choice([0, 1], 1, p=[1 - p, p])
        if update == 1:
            cell = board.choose_random_used_cell()
            board.fix_board_remove_symbol(cell)
        else:
            board.fix_cell()



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

CellAndSymbol_Absorbers_metropolis_RLS(board, _lambda)

