import sys
import numpy as np
import timeit
import csv
import random

params = {
    "unmarked_cells" : 0,
    'max_marked_cell' : 0
}

global N
N = int(sys.argv[1])

global cluster_path
cluster_path = '/cs/usr/tamarals/Documents/N_queens_problem/ColoringGraph/'

global output_dir
output_dir = 'N_' + sys.argv[1] +'/'

global board
board = np.zeros(N**2).reshape((N, N))

global empty_cells
empty_cells = []

global original_empty_cells
original_empty_cells = []

global start
start = timeit.default_timer()

def print_solution(file = None):
    for i in range(N):
        line = ''
        for s in board[i]:
            if s == 0:
                line == '-- '
            else:
                line += "{:02d}".format(int(s))
                line += " "
        if file == None:
            print(line)
        else:
            line += '\n'
            file.write(line)

#read random greedy board from file
def read_board():
    csv_file_name = cluster_path + output_dir + 'board_' + str(N) + '.csv'

    #get board
    with open(csv_file_name) as file:
        reader = csv.reader(file, quoting = csv.QUOTE_NONNUMERIC)
        count = 0
        for row in reader:
            board[count] = row
            count += 1

#find empty cells in board
def find_empty_cells():
   for r in range(N):
        for c in range(N):
            if board[r][c] == 0:
                empty_cells.append((r,c))
                params['unmarked_cells'] += 1

   original_empty_cells = empty_cells.copy()
   params['max_marked_cell'] = N**2 - params['unmarked_cells']

#find missing symbols from single row in board
def find_row_missing_symbols(row, cell):

    symbols = [s for s in range(1, N + 1)]
    for i, symbol in enumerate(board[row]):
        if not int(symbol) == 0:
            symbols.remove(int(symbol))

    if len(symbols) == 0:
        print('here')

    return symbols

def find_symbol_in_col(col, symbol):

    for row in range(N):
        col_symbol  = int(board[row][col])
        if col_symbol == symbol:
            return row

    return 0

def find_symbol_in_diagonal(cell, symbol):
    (row,col) = cell
    diagonal_places = []

    # Check left diagonal on upeer side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] == symbol:
            diagonal_places.append((i,j))

    # Check left diagonal on lower side
    for i, j in zip(range(row, N, 1),
                    range(col, -1, -1)):
        if board[i][j] == symbol:
            diagonal_places.append((i,j))

    # Check right diagonal on upper side
    for i, j in zip(range(row, -1, -1),
                    range(col, N, 1)):
        if board[i][j] == symbol:
            diagonal_places.append((i,j))

    # Check right diagonal on upper side
    for i, j in zip(range(row, N, 1),
                    range(col, N, 1)):
        if board[i][j] == symbol:
            diagonal_places.append((i,j))

    return diagonal_places

def empty_single_cell(cell):
    (row,col) = cell
    board[row][col] = 0
    empty_cells.append((row, col))
    params['unmarked_cells'] += 1

def find_threatning_cells(cell, symbol):
    (row,col) = cell
    threat_cells = []

    #check col
    _row = find_symbol_in_col(col, symbol)
    if _row > 0:
        threat_cells.append((_row, col))

    #check diagonal
    threat_cells = threat_cells + find_symbol_in_diagonal(cell, symbol)

    return threat_cells

def choose_best_symbol(optional_symbols, threat_len):
    symbols = []
    min_threat = min(threat_len)
    for i, l in enumerate(threat_len):
        if l == min_threat:
            symbols.append(optional_symbols[i])

    return random.choice(symbols)

def fix_board_max():
    while params['unmarked_cells'] > 0:
        cell = random.choice(empty_cells)
        (row,col) = cell

        threats = {}
        threat_len = []

        optional_symbols = find_row_missing_symbols(row, cell)
        for symbol in optional_symbols:
            threats[symbol] = find_threatning_cells(cell, symbol)
            threat_len.append(len(threats[symbol]))

        symbol = choose_best_symbol(optional_symbols, threat_len)

        for t in threats[symbol]:
            empty_single_cell(t)

        #place symbol in board
        board[row][col] = symbol
        empty_cells.remove(cell)
        params['unmarked_cells'] -= 1

        if N**2 - params['unmarked_cells'] > params['max_marked_cell']:
            print('max cells count ', N**2 - params['unmarked_cells'])
            params['max_marked_cell'] = N**2 - params['unmarked_cells']

def fix_board():

    while params['unmarked_cells'] > 0:
        cell = random.choice(empty_cells)
        (row,col) = cell
        count_swap = 0

        #find optional symbols to place in row
        optional_symbols = find_row_missing_symbols(row, cell)
        symbol = random.choice(optional_symbols)

        #find symbol in col
        symbol_row = find_symbol_in_col(col, symbol)
        if symbol_row > 0:
            #print('replace in col!')
            empty_single_cell((symbol_row, col))
            count_swap += 1

        #find symbol in diagonal
        symbol_diagonal = find_symbol_in_diagonal(cell, symbol)
        if len(symbol_diagonal) > 0:
            #print('replace in ', len(symbol_diagonal), ' places in diagonals.')
            for diag_cell in symbol_diagonal:
                empty_single_cell(diag_cell)
                count_swap +=1

        #place symbol in board
        board[row][col] = symbol
        empty_cells.remove(cell)
        params['unmarked_cells'] -= 1

        if N**2 - params['unmarked_cells'] > params['max_marked_cell']:
            print('max cells count ', N**2 - params['unmarked_cells'])
            params['max_marked_cell'] = N**2 - params['unmarked_cells']

#main
#initialize the board with reading from file
read_board()
#find empty cells in board
find_empty_cells()

#start swapping cells
#fix_board()
fix_board_max()

print_solution()
end = timeit.default_timer()
print('running time- ', (end - start), ' sec.')
