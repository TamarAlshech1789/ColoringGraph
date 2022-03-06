import numpy as np
import sys
import copy
from board import Board
from read_board import read_board
from random_greedy import random_greedy


def metropolis_RLS(board, _lambda):
    N = board.N
    board.MMC_empty_cells = copy.deepcopy(board.empty_cells)
    while board.marked_cells < N **2:
        board.fix_cell()



#input params are:
# N     lambda      is_cluster      read_board
N = int(sys.argv[1])
#_lambda = float(sys.argv[2])
_lambda = N ** 2
#is_cluster = sys.argv[3] == '1'
is_cluster = False
#_read_board = sys.argv[4] == '1'
_read_board = False

if _read_board:
    board = Board(N=N, is_cluster=is_cluster, _lambda=_lambda)
    read_board(board)
else:
    board = random_greedy(N=N, is_cluster=is_cluster, _lambda=_lambda)

metropolis_RLS(board, _lambda)

