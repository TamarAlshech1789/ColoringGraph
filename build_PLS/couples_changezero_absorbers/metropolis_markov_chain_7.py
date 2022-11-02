import numpy as np
import sys
import copy
from board import Board
from read_board import read_board
from random_greedy import random_greedy

def CellAndSymbol_SwitchZero_Absorbers_metropolis_RLS(board, lambda_1, lambda_2):
    N = board.N
    board.MMC_empty_cells = copy.deepcopy(board.empty_cells)
    p = 1 / lambda_1

    while board.marked_cells < N ** 2:
        #update = np.random.choice([0, 1], 1, p=[1 - p, p])
        update = 0
        if update == 1:
            cell = board.choose_random_used_cell()
            board.fix_board_remove_symbol(cell)
        else:
            update = np.random.choice([0, 1], 1, p=[1 - 1 / lambda_2, 1 / lambda_2])
            if update == 1:
                board.switch_empty_cell()
                board.switch_empty_cell_with_one_or_two()
            else:
                board.fix_cell()

#input params are:
# N     lambda      is_cluster      read_board
#N = int(sys.argv[1])
num_board = sys.argv[1]
#lambda_1 = float(sys.argv[2])
lambda_1 = 0
lambda_2 = float(sys.argv[2])
#_lambda = N ** 2
#is_cluster = sys.argv[3] == '1'
is_cluster = True
#_read_board = sys.argv[4] == '1'
_read_board = False

if _read_board:
    board = Board(N=N, is_cluster=is_cluster, _lambda=lambda_2)
    board_file_name = '/cs/labs/nati/tamarals/27/list_27/27_' + num_board + '.txt'
    read_board(board, board_file_name)
else:
    board = random_greedy(N=N, is_cluster=is_cluster, _lambda=lambda_1)

CellAndSymbol_SwitchZero_Absorbers_metropolis_RLS(board, lambda_1, lambda_2)
