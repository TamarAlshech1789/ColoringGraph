import sys
import numpy as np
import random
import timeit
from enum import Enum
import os.path
import csv

class SelectingSymbolMethod(Enum):
    metropolis    = 1
    random_symbol = 2
    prob_symbol   = 3

params = {
    'lambda' : int(sys.argv[2]),
    'N': int(sys.argv[1]),
    'marked_cells' : 0,
    'max_marked_cells' : 0,
    'max_cover_per' : 0,
    'num_iteretions' : 0,
    'num_changing_num_to_0' : 0,
    'num_changing_0_to_num' : 0,
    'num_changing_num_to_num' : 0
}
global start
start = timeit.default_timer()

global file_name
file_name = ''

global file

global select_symbol
select_symbol = SelectingSymbolMethod.metropolis

global board
board = np.zeros(params['N']**2).reshape((params['N'], params['N']))

global all_indices
all_indices = list(np.ndindex(board.shape))

global cluster_path
cluster_path = '/cs/usr/tamarals/Documents/N_queens_problem/ColoringGraph/'

global output_dir
output_dir = 'N_' + sys.argv[1] +'/'


def print_solution(file = None):
    for i in range(params['N']):
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

#find all possible symbol for a single cell
def find_possible_symbols(cell, update_params = False):
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
    """
    if update_params == True:
        if len(symbols) == 0:
            if not cell in params['no_options_cells']:
                params['num_no_options'] += 1
                params['no_options_cells'].append(cell)
        else:
            params['num_no_options'] = 0
            params['no_options_cells'] = []
    """
    return symbols

def get_probability(symbols, symbol, board_cell):
    sum_lambda = 0.0
    curr_lambda = 0.0
    exponent = params['marked_cells']
    min_exponent = exponent
    min_exponent = params['lambda_power'] * (exponent)
    if board_cell > 0:
        min_exponent -= 1
        min_exponent = params['lambda_power'] * (exponent - 1)

    for s in symbols:
        add = 0.0
        if s == 0:
            if board_cell == 0:
                add = 10 ** (params['lambda_power'] * (exponent) - min_exponent)
            else:
                add = 10 ** (params['lambda_power'] * (exponent - 1) - min_exponent)
            if s == symbol:
                curr_lambda = add
        else:
            if board_cell == 0:
                add = 10 ** (params['lambda_power'] * (exponent + 1) - min_exponent)
            else:
                add = 10 ** (params['lambda_power'] * (exponent) - min_exponent)
            if s == symbol:
                curr_lambda = add
        sum_lambda += add

    return curr_lambda / sum_lambda

def update_params(cell, symbol):
    if board[cell[0]][cell[1]] == 0:
        if symbol > 0:
            params['marked_cells'] += 1
            params['num_changing_0_to_num'] += 1
    else:
        if symbol == 0:
            params['marked_cells'] -= 1
            params['num_changing_num_to_0'] += 1
        elif not symbol == board[cell[0]][cell[1]]:
            params['num_changing_num_to_num'] += 1

    board[cell[0]][cell[1]] = symbol
    if params['max_marked_cells'] < params['marked_cells']:
        cover_per = float(100 * params['marked_cells']) / N**2
        if (cover_per - params['max_cover_per']) >= 0.2:
            with open(csv_file_name, 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([timeit.default_timer() - start, cover_per])

            if float(100 * params['marked_cells']) / N**2 > 95:
                file = open(file_name, 'a')

                file.write(str(cover_per) + ' per.         at time ' + str(timeit.default_timer() - start) +'\n')
                if int(cover_per * 100)%10 - int(params['max_cover_per'] * 100)%10 >= 1:
                    file.write('*****************************************************\n')
                    file.write('board with ' + str(int(cover_per)) + ' per cover:\n')
                    print_solution(file)
                    file.write('*****************************************************\n')
                file.close()

            params['max_cover_per'] = cover_per

        params['max_marked_cells'] = params['marked_cells']
    params['num_iteretions'] += 1

def metropolis_RLS():
    #params['num_no_options'] < stop_condition * params['N'] ** 2 and
    while(params['marked_cells'] < N ** 2 ):
        cell = random.choice(all_indices)
        row,col = cell
        cell_symbol = board[row][col]

        if select_symbol == SelectingSymbolMethod.metropolis:
            possible_symbols = find_possible_symbols(cell, True)
            if len(possible_symbols) > 0:
                symbol = random.choice(possible_symbols)
                update_params(cell, symbol)
            else:
                if cell_symbol > 0:
                    p = 1 / params['lambda']
                    update = np.random.choice([0, 1], 1, p=[1 - p, p])
                    if update == 1:
                        update_params(cell, 0)

        """else:
            # get possible values
            possible_symbols = find_possible_symbols(cell, True, True)
            possible_symbols.append(0)
            if cell_symbol > 0:
                possible_symbols.append(cell_symbol)

            if select_symbol == SelectingSymbolMethod.prob_symbol:
                p_vec = [get_probability(possible_symbols, s, cell_symbol) for s in possible_symbols]
                symbol = np.random.choice(possible_symbols, 1, p=p_vec)
                update_params(cell, symbol)
            #picking symbol randomally
            else:
                symbol = random.choice(possible_symbols)
                if not symbol == cell_symbol:
                    p = get_probability(possible_symbols, symbol, cell_symbol)
                    update = np.random.choice([0,1], 1, p=[1 - p, p])

                    if update == 1:
                        update_params(cell, symbol)"""

def read_board():
    csv_file_name = output_dir + 'board_' + str(N) + '.csv'
    txt_file_name = output_dir + 'board_' + str(N) + '_num_of_queens.txt'

    with open(csv_file_name) as file:
        reader = csv.reader(file, quoting = csv.QUOTE_NONNUMERIC)
        count = 0
        for row in reader:
            board[count] = row
            count += 1

    with open(txt_file_name) as txt_file:
        params['marked_cells'] = int(txt_file.readline().rstrip('\n'))

def init_all_params(N):
    params['N'] = N
    params['num_iteretions'] = 0
    params['max_marked_cells'] = 0
    """
    params['num_no_options'] = 0
    params['no_options_cells'] = []
    """
    params['num_iteretions'] = 0
    params['num_changing_0'] = 0

    """for i in range(params['N']):
        board[i][i] = i + 1
        # board[i][params['N'] - i - 1] = (i + 2) % params['N'] + 1"""
    read_board()

N = int(sys.argv[1])
#e = int(sys.argv[2])
params['lambda'] = int(sys.argv[2])

#params['lambda'] = 10**e
file_name = output_dir + 'metropolis_board_N_' +  str(params['N']) + '_lambda_' + str(params['lambda']) + '.txt'

print('running until board is full!')
print('*****************************************************')
print(file_name)
print('*****************************************************')

if len(sys.argv) < 4:
    output_dir = cluster_path + output_dir

init_all_params(N)

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)


if os.path.isfile(file_name):
    os.remove(file_name)
file = open(file_name, 'a')

csv_file_name = output_dir + 'N_' + str(params['N']) + '_lambda_' +str(params['lambda']) + '.csv'
if os.path.isfile(csv_file_name):
    os.remove(csv_file_name)

with open(csv_file_name, 'a',) as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Time (sec)', 'Per. cover'])

file.write('fill precentages of the board\n')
file.close()
#sys.stdout = open(file_name, "w")

metropolis_RLS()
print('number of placements -', params['marked_cells'])
print('cover ', float(params['marked_cells']) / N**2, ' per. of the cells')
print_solution()
end = timeit.default_timer()
print('running time- ', (end - start), ' sec.')
print('*****************************************************')
print('number of changes 0 to num-', params['num_changing_0_to_num'], ' times')
print('number of changes num to 0-', params['num_changing_num_to_0'], ' times')
print('number of changes num to num-', params['num_changing_num_to_num'], ' times')

#sys.stdout.close()
