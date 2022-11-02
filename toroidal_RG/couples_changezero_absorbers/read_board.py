import csv
from board import Board
from cell import Cell

def read_board(board, file_name=''):

    if file_name == '':
        board_file_name = board.output_dr + 'board_' + str(board.N) + '.csv'
    else:
        board_file_name = file_name

    count = 0
    if board_file_name.split('.')[-1] == 'txt':
        unmarked_cells = 0
        with open(board_file_name) as file:
            lines = file.readlines()
            for row in lines:
                symbols = row.split(' ')
                if symbols[-1] == '\n':
                    symbols = symbols[:-1]
                for s in symbols:
                    cell = board.empty_cells[count]
                    if not s == '--':
                        s = int(s)
                        board.fix_board_add_symbol(cell, s, random_greedy=True)
                    else:
                        unmarked_cells += 1
                        count+= 1

    else:
        count = 0
        unmarked_cells = 0
        with open(board_file_name) as file:
            reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                for s in row:
                    cell = board.empty_cells[count]
                    count += 1

                    board.fix_board_add_symbol(cell, s)
                    if s == 0:
                        unmarked_cells += 1

    board.marked_cells = board.N ** 2 - unmarked_cells
