import sys
import numpy as np
import random
import timeit

params = {
    'lambda' : 10**int(sys.argv[2]),
    'lambda_power' : int(sys.argv[2]),
    'N': int(sys.argv[1]),
    'marked_cells' : 0,
    'max_marked_cells' : 0,
    'num_no_options' : 0,
    'no_options_cells' : [],
    'num_iteretions' : 0,
    'num_changing_num_to_0' : 0,
    'num_changing_0_to_num' : 0,
    'num_changing_num_to_num' : 0
}

global pick_with_prob
pick_with_prob = False

global board
board = np.zeros(params['N']**2).reshape((params['N'], params['N']))

global indices
indices = list(np.ndindex(board.shape))

global all_indices
all_indices = list(np.ndindex(board.shape))

global used_indices
used_indices = []

global cant_place_indices
cant_place_indices = []

global occupied_cells_rows, occupied_cells_cols
occupied_cells_rows = [[] for i in range(params['N'])]
occupied_cells_cols = [[] for i in range(params['N'])]


def choose_random_cell():
    cell = random.choice(indices)
    while(board[cell[0]][cell[1]] != 0):
        cell = random.choice(indices)

    return cell

def choose_random_color(cell):
    colors = list(range(1, N+1))
    (row, col) = cell

    for r in occupied_cells_cols[col]:
        if board[r][col] in colors :
            colors.remove(board[r][col])
    for c in occupied_cells_rows[row]:
        if board[row][c] in colors :
            colors.remove(board[row][c])

    # Check left diagonal on upeer side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] in colors:
            colors.remove(board[i][j])

    # Check left diagonal on lower side
    for i, j in zip(range(row, N, 1),
                    range(col, -1, -1)):
        if board[i][j] in colors:
            colors.remove(board[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, -1, -1),
                    range(col, N, 1)):
        if board[i][j] in colors:
            colors.remove(board[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, N, 1),
                    range(col, N, 1)):
        if board[i][j] in colors:
            colors.remove(board[i][j])

    if len(colors) == 0:
        return 0

    return random.choice(colors)

def find_set_of_absorbers(cell):
    B = []
    colors = []
    (row, col) = cell
    for c in occupied_cells_rows[row]:
        if board[row][c] in colors :
            colors.appennd(board[row][c])

    return B

def find_absorber(cell):
    B = find_set_of_absorbers(cell)
    return random.choice(B)

def random_greedy():
    # Get a list of indices for an array of this shape#Get a list of indices for an array of this shape
    queen_count = 0

    while queen_count < 0.7 * (N ** 2):
        cell = choose_random_cell()
        color = choose_random_color(cell)
        if color == 0:
            cant_place_indices.append(cell)
            indices.remove(cell)
        else:
            board[cell[0]][cell[1]] = color
            occupied_cells_cols[cell[1]].append(cell[0])
            occupied_cells_rows[cell[0]].append(cell[1])
            indices.remove(cell)
            used_indices.append(cell)
            queen_count += 1

    return board, queen_count

def print_solution():
    for i in range(params['N']):
        line = ""
        for j in range(params['N']):
            if board[i][j] == 0:
                line += '-- '
            else:
                line += "{:02d}".format(int(board[i][j]))
                line += " "
        print(line)

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
    if board[row][col] > 0:
        symbols.append(board[row][col])
    return symbols

def get_probability(symbols, symbol, board_cell):
    sum_lambda = 0.0
    curr_lambda = 0.0
    exponent = params['marked_cells']
    min_exponent = params['lambda_power'] * (exponent)
    if board_cell > 0:
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
    params['max_marked_cells'] = max(params['max_marked_cells'], params['marked_cells'])
    params['num_iteretions'] += 1

def metropolis_RLS():
    while(params['num_no_options'] < 0.9 * params['N'] ** 2 and params['marked_cells'] < N ** 2 ):
        cell = random.choice(all_indices)
        possible_symbols = find_possible_symbols(cell)
        if(pick_with_prob == True):
            p_vec = [get_probability(possible_symbols, s, board[cell[0]][cell[1]]) for s in possible_symbols]
            symbol = np.random.choice(possible_symbols, 1, p=p_vec)
            update_params(cell, symbol)

        else:
            symbol = random.choice(possible_symbols)
            if not symbol == board[cell[0]][cell[1]]:
                p = get_probability(possible_symbols, symbol, board[cell[0]][cell[1]])
                update = np.random.choice([0,1], 1, p=[1 - p, p])

                if update == 1:
                    update_params(cell, symbol)


def init_all_params(N, e):
    # initial params
    params['N'] = N
    params['lambda_power'] = e
    params['num_iteretions'] = 0
    params['max_marked_cells'] = 0
    params['num_no_options'] = 0
    params['no_options_cells'] = []
    params['num_iteretions'] = 0
    params['num_changing_0'] = 0

    """for i in range(params['N']):
        board[i][i] = i + 1
        # board[i][params['N'] - i - 1] = (i + 2) % params['N'] + 1"""
    board, params['marked_cells'] = random_greedy()


N = int(sys.argv[1])
e = int(sys.argv[2])

#for N in range(20, 100, 20):
    #for e in range(2,10):
init_all_params(N, e)

params['lambda'] = 10**e
file_name = 'metropolis_borad_N_' +  str(params['N']) + '_lambda_10e' + str(e) + '.txt'
#sys.stdout = open(file_name, "w")
start = timeit.default_timer()
metropolis_RLS()
print('running until board is full!')
print('*****************************************************')
print(file_name)
print('*****************************************************')
print('number of placements -', params['marked_cells'])
print('cover ', params['marked_cells'] / N**2, ' per. of the cells')
print_solution()
end = timeit.default_timer()
print('running time- ', (end - start), ' sec.')
print('*****************************************************')
print('number of changes 0 to num-', params['num_changing_0_to_num'], ' times')
print('number of changes num to 0-', params['num_changing_num_to_0'], ' times')
print('number of changes num to num-', params['num_changing_num_to_num'], ' times')

#sys.stdout.close()
