from board import Board
import sys
import csv

def random_greedy(N, is_cluster=True, _lambda = 0):
    # Get a list of indices for an array of this shape#Get a list of indices for an array of this shape

    board = Board(N, is_cluster, _lambda)

    while len(board.RG_empty_cells) > 0:
        cell = board.choose_random_empty_cell()
        symbol = board[cell].choose_random_symbol()

        if symbol == 0:
            board.RG_empty_cells.remove(cell)
        else:
            board.fix_board_add_symbol(cell, symbol)
            board.RG_empty_cells.remove(cell)
            board.used_indices.append(cell)

    #board.print_solution()
    #print('**************************************************')
    return board.marked_cells

N = int(sys.argv[1])
num_repeats = 100
csv_file_name = '/cs/usr/tamarals/Documents/N_queens_problem/ColoringGraph/check_random_greedy/results.csv'
for repeat in num_repeats:
    marked_cells = random_greedy(N, True, 0)
    cover_per = float(100 * marked_cells) / N ** 2
    with open(csv_file_name, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([int(repeat), cover_per])