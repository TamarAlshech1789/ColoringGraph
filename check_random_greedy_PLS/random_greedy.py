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
    return board

board = random_greedy(20, is_cluster = False)
board.check_pandiagonals()
print('number of empty cells - ', board.N**2 - board.marked_cells)
board.print_solution()
