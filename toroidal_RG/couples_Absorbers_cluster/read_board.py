import csv
from board import Board
from cell import Cell

def read_board(board, file_name=''):

    if file_name == '':
        board_file_name = board.output_dr + 'board_' + str(board.N) + '.csv'
    else:
        board_file_name = file_name

    count = 0
    unmarked_cells = 0
    with open(board_file_name) as file:
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            for s in row:
                cell = board.empty_cells[count]
                count += 1

                board.set_cell(cell, s)
                board.fix_board(cell, s)
                if s == 0:
                    unmarked_cells += 1

    board.marked_cells = board.N ** 2 - unmarked_cells


def read_board_txt(board, board_file_name, percent = 100):

    N = board.N
    count = 0
    unmarked_cells = 0
    first = False
    with open(board_file_name) as f:
        lines = f.readlines()
        for row in lines:
            if first == True:
                first = False
            else:
                if row[-1] == '\n':
                    row = row[:-1]
                row = row.split()
                for s in row:
                    cell = board.empty_cells[0]
                    if not s == '--':
                        s = int(s)
                        board.fix_board_add_symbol(cell, s)

                    count += 1
                    """
                    if count >= (percent / 100) * N **2 :
                        board.marked_cells = count
                        return
                    """

    #board.marked_cells = count



