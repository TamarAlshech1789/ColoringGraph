import sys
import numpy as np
import random
from colorama import Fore
import timeit

params = {
    'lambda' : 10**3,
    'N': 50,
    'marked_cells' : 0,
    'max_marked_cells' : 0,
    'num_no_options' : 0,
    'no_options_cells' : [],
    'num_iteretions' : 0
}

global board
board = np.zeros(params['N']**2).reshape((params['N'], params['N']))

global indices
indices = list(np.ndindex(board.shape))

def print_solution():
    for i in range(params['N']):
        for j in range(params['N']):
            if board[i][j] == 0:
                print('--', end=" ")
            else:
                print("{:02d}".format(int(board[i][j])), end=" ")
        print()

#find all possible symbol for a single cell
def find_possible_symbols(cell):
    symbols = list(range(1, params['N']+1))
    (row, col) = cell

    for r in range(params['N']):
        if not r == row and board[r][col] in symbols :
            symbols.remove(board[r][col])
    for c in range(params['N']):
        if not c == col and board[row][c] in symbols:
            symbols.remove(board[row][c])

    # Check left diagonal on upeer side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    # Check left diagonal on lower side
    for i, j in zip(range(row, params['N'], 1),
                    range(col, -1, -1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, -1, -1),
                    range(col, params['N'], 1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, params['N'], 1),
                    range(col, params['N'], 1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    if len(symbols) == 0:
        if not cell in params['no_options_cells']:
            params['num_no_options'] += 1
            params['no_options_cells'].append(cell)
    else:
        params['num_no_options'] = 0
        params['no_options_cells'] = []

    symbols.append(0)
    symbols.append(board[row][col])
    return symbols

def get_probability(symbols, symbol, board_cell):
    sum_lambda = 0
    curr_lambda = 0
    exponent = params['marked_cells']

    for s in symbols:
        add = 0
        if s == 0:
            if board_cell == 0:
                add = params['lambda'] ** (exponent)
            else:
                add = params['lambda'] ** (exponent - 1)
            if s == symbol:
                curr_lambda = add
        else:
            if board_cell == 0:
                add = params['lambda'] ** (exponent + 1)
            else:
                add = params['lambda'] ** (exponent)
            if s == symbol:
                curr_lambda = add
        sum_lambda += add

    return curr_lambda / sum_lambda

def metropolis_RLS():
    while(params['num_no_options'] < 0.85 * params['N'] ** 2 ):
        cell = random.choice(indices)
        possible_symbols = find_possible_symbols(cell)
        symbol = random.choice(possible_symbols)
        p = get_probability(possible_symbols, symbol, board[cell[0]][cell[1]])
        update = np.random.choice([0,1], 1, p=[1 - p, p])

        if update == 1:
            if board[cell[0]][cell[1]] == 0 and symbol > 0:
                params['marked_cells'] += 1
            if board[cell[0]][cell[1]] > 0 and symbol == 0:
                params['marked_cells'] -= 1
            board[cell[0]][cell[1]] = symbol
        params['max_marked_cells'] = max(params['max_marked_cells'], params['marked_cells'])
        params['num_iteretions'] += 1

for N in range(20, 100, 20):
    for e in range(2,10):
        #initial params
        params['N'] = N
        params['num_iteretions'] = 0
        params['marked_cells'] = params['N']
        params['max_marked_cells'] = 0
        params['num_no_options'] = 0
        params['no_options_cells'] = []
        params['num_iteretions'] = 0

        board = np.zeros(params['N'] ** 2).reshape((params['N'], params['N']))
        for i in range(params['N']):
            board[i][i] = i + 1
            # board[i][params['N'] - i - 1] = (i + 2) % params['N'] + 1
        indices = list(np.ndindex(board.shape))


        params['lambda'] = 10**e
        file_name = 'metropolis_borad_N_' +  str(params['N']) + '_lambda_10e' + str(e) + '.txt'
        #sys.stdout = open(file_name, "w")
        start = timeit.default_timer()
        metropolis_RLS()
        print('*****************************************************')
        print('number of placements -', params['marked_cells'])
        print('cover ', params['marked_cells'] / N**2, ' per. of the cells')
        print_solution()
        end = timeit.default_timer()
        print('running time- ', (end - start), ' sec.')

        #sys.stdout.close()
