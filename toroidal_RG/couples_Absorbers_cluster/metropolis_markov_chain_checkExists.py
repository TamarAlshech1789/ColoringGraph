import numpy as np
import sys
import copy
from board import Board
from read_board import read_board, read_board_txt
from random_greedy import random_greedy
import timeit

def CellAndSymbol_Absorbers_metropolis_RLS(boards, num_boards):
    N = boards[0].N
    num_boards = list(num_boards)
    for i in num_boards:
        boards[i].MMC_empty_cells = copy.deepcopy(boards[i].empty_cells)


    while len(num_boards)> 0:
        curr_num_boards = list(num_boards)
        for i in curr_num_boards:
            if boards[i].marked_cells == N ** 2 :
                boards[i].print_current_board(100)
                num_boards.remove(i)

            p = 1 / boards[i]._lambda
            update = np.random.choice([0, 1], 1, p=[1 - p, p])
            if update == 1:
                cell = boards[i].choose_random_used_cell()
                boards[i].fix_board_remove_symbol(cell)
            else:
                boards[i].fix_cell()

            if boards[i].marked_cells == N ** 2 and i in num_boards:
                boards[i].print_current_board(100)
                num_boards.remove(i)



#input params are:
# N     lambda      is_cluster      read_board
N = int(sys.argv[1])
if len(sys.argv > 2):
    _lambda = float(sys.argv[2])
#_lambda = N ** 2
#is_cluster = sys.argv[3] == '1'
is_cluster = True
#_read_board = sys.argv[4] == '1'
_read_board = True

boards = []
epsilons = [float(N), 90, 270, 450, 900, 1800]
percents = [(i+1) * 10 for i in range(9)]
pairs = []

num_boards = range(len(pairs))

if _read_board:
    count = 1
    for i in num_boards:
        for epsilon in epsilons:
            file_name = "boards/" + str(N) + '_'+ str(i + 1) + '.txt'
            board = Board(N, is_cluster, epsilon, count)
            read_board_txt(board, file_name)
            boards.append(board)
            count += 1
else:
    for i in num_boards:
        board  = random_greedy(N=N, is_cluster=is_cluster, _lambda=_lambda, count=i+1)
        boards.append(board)

for i in num_boards:
    boards[i].start_time = timeit.default_timer()
CellAndSymbol_Absorbers_metropolis_RLS(boards, num_boards)



