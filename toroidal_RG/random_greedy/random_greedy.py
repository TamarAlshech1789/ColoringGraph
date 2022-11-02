import random
from colorama import Fore
from board import Board
from read_board import read_board
import csv
import sys

def random_greedy(N, is_cluster=False, _lambda = 0):
    # Get a list of indices for an array of this shape#Get a list of indices for an array of this shape

    board = Board(N, is_cluster, _lambda)

    while len(board.RG_empty_cells) > 0:
        cell = board.choose_random_empty_cell()
        symbol = board[cell].choose_random_toroidal_symbol()

        if symbol == 0:
            board.RG_empty_cells.remove(cell)
        else:
            board.fix_board_add_symbol(cell, symbol)
            board.RG_empty_cells.remove(cell)

    board.change_random_greedy_stage()
    file = open(board.output_dir + "RG_board_" + str(board.N) + "_" + str(int(board._lambda)) + ".txt", "a")
    board.print_solution(file)
    print('**************************************************')
    return board.marked_cells


N = int(sys.argv[1])
num_repeats = 5
original_csv_file_name = '/cs/labs/nati/tamarals/toroidal_updates/check_random_greedy/N_' + str(N) + '_' 
for repeat in range(5,7):
    csv_file_name = original_csv_file_name + str(repeat) + '.csv'
    marked_cells = random_greedy(N, True, 0)
    print(marked_cells)
    cover_per = float(100 * marked_cells) / N ** 2
    with open(csv_file_name, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([int(repeat), cover_per])

