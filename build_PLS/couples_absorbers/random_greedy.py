import random
from colorama import Fore
from board import Board
from read_board import read_board
import sys

def random_greedy(N, is_cluster=False, _lambda = 0, count = 0):
    # Get a list of indices for an array of this shape#Get a list of indices for an array of this shape

    board = Board(N, is_cluster, _lambda, count)

    while len(board.RG_empty_cells) > 0:
        cell = board.choose_random_empty_cell()
        symbol = board[cell].choose_random_symbol()

        if symbol == 0:
            board.RG_empty_cells.remove(cell)
        else:
            board.fix_board_add_symbol(cell, symbol)
            board.RG_empty_cells.remove(cell)

    board.change_random_greedy_stage()
    file = open(board.output_dir + "RG_board_" + str(board.N) + "_" + str(int(board._lambda)) + ".txt", "a")
    board.print_solution(file)
    print('**************************************************')
    return board

