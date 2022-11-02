import numpy as np
import sys
from board import Board
from read_board import read_board
from random_greedy import random_greedy
import timeit

def list_available_CellAndSymbol_metropolis_RLS(boards, num_boards):
	N = boards[0].N
	i = 0

	while len(num_boards)> 0:
		for i in num_boards:
			p = 1 / boards[i]._lambda
			update = np.random.choice([0, 1], 1, p=[1 - p, p])
			if update == 1:
				cell = boards[i].choose_random_used_cell()
				boards[i].fix_board_remove_symbol(cell)
			else:
				(cell, symbol) = boards[i].choose_good_random_cell_and_symbol()
				if cell == (-1,-1):
					cell = boards[i].choose_random_used_cell()
					boards[i].fix_board_remove_symbol(cell)

				else:
					if boards[i][cell].symbol == 0:
						boards[i].fix_board_add_symbol(cell, symbol)
					else:
						boards[i].fix_board_change_symbol(cell, symbol)

			if boards[i].marked_cells == N ** 2:
				num_boards.remove(i)
#input params are:
# N     lambda      is_cluster      read_board
N = int(sys.argv[1])
_lambda = float(sys.argv[2])
#_lambda = N ** 2
#is_cluster = sys.argv[3] == '1'
is_cluster = True
#_read_board = sys.argv[4] == '1'
_read_board = False

boards = []
num_boards = range(5)
if _read_board:
	boards = Board(N=N, is_cluster=is_cluster, _lambda=_lambda)
	read_board(boards)
else:
	boards = [random_greedy(N=N, is_cluster=is_cluster, _lambda=_lambda, count=i + 1) for i in num_boards]


for i in num_boards:
	boards[i].start_time = timeit.default_timer()
list_available_CellAndSymbol_metropolis_RLS(boards, num_boards)

