import numpy as np
import random
import copy
from colorama import Fore
import timeit
import os
import sys

global N
N = int(sys.argv[1])

global print_board
print_board = True

global queen_borad
queen_borad = np.zeros(N**2).reshape((N, N))

global indices
indices = list(np.ndindex(queen_borad.shape))

global used_indices
used_indices = copy.deepcopy(indices)

global cant_place_indices
cant_place_indices = []

global occupied_cells_rows, occupied_cells_cols
occupied_cells_rows = [[] for i in range(N)]
occupied_cells_cols = [[] for i in range(N)]

global output_dir
output_dir = 'N_' + str(N) +'/'

def choose_random_cell():
    cell = random.choice(indices)
    while(queen_borad[cell[0]][cell[1]] != 0):
        cell = random.choice(indices)

    return cell

def print_solution():
    for i in range(N):
        for j in range(N):
            if queen_borad[i][j] == 0:
                print(Fore.RED, '--', end=" ")
            else:
                print(Fore.WHITE, "{:02d}".format(int(queen_borad[i][j])), end=" ")
        print()


def choose_random_color(cell):
    colors = list(range(1, N+1))
    (row, col) = cell

    for r in occupied_cells_cols[col]:
        if queen_borad[r][col] in colors :
            colors.remove(queen_borad[r][col])
    for c in occupied_cells_rows[row]:
        if queen_borad[row][c] in colors :
            colors.remove(queen_borad[row][c])

    # Check left diagonal on upeer side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if queen_borad[i][j] in colors:
            colors.remove(queen_borad[i][j])

    # Check left diagonal on lower side
    for i, j in zip(range(row, N, 1),
                    range(col, -1, -1)):
        if queen_borad[i][j] in colors:
            colors.remove(queen_borad[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, -1, -1),
                    range(col, N, 1)):
        if queen_borad[i][j] in colors:
            colors.remove(queen_borad[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, N, 1),
                    range(col, N, 1)):
        if queen_borad[i][j] in colors:
            colors.remove(queen_borad[i][j])

    if len(colors) == 0:
        return 0

    return random.choice(colors)

def random_greedy():
    # Get a list of indices for an array of this shape#Get a list of indices for an array of this shape
    queen_count = 0

    while len(indices) > 0:
        cell = choose_random_cell()
        color = choose_random_color(cell)
        if color == 0:
            #print('error - no option for coloring cell ', cell)
            #print('number of queens placed until now - ', queen_count, ' out for ', N**2)
            #print('curr board - ')
            #print_solution()
            cant_place_indices.append(cell)
            indices.remove(cell)
        else:
            queen_borad[cell[0]][cell[1]] = color
            occupied_cells_cols[cell[1]].append(cell[0])
            occupied_cells_rows[cell[0]].append(cell[1])
            indices.remove(cell)
            used_indices.append(cell)
            queen_count += 1

    if queen_count == N**2:
        print('success! all queens are replaced!')

    if(print_board):
        print('queens board - ')
        print_solution()

        csv_file_name = output_dir + 'board_' + str(N) + '.csv'
        np.savetxt(csv_file_name, queen_borad, delimiter = ',')

        txt_file_name = output_dir + 'board_' + str(N) + '_num_of_queens.txt'
        with open(txt_file_name, 'w') as txt_file:
            txt_file.write('%d' % queen_count)

    return queen_count / N**2

start = timeit.default_timer()
num_of_repeat = 1
prob = []

if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

print(Fore.WHITE, '*****************************************************')
print(Fore.WHITE, 'for N =', N, ', and', num_of_repeat, ' repeats:')

for i in range(num_of_repeat):
    queen_borad = np.zeros(N ** 2).reshape((N, N))
    indices = list(np.ndindex(queen_borad.shape))
    used_indices = []
    cant_place_indices = []
    occupied_cells_rows = [[] for i in range(N)]
    occupied_cells_cols = [[] for i in range(N)]

    prob.append(random_greedy())
    print(Fore.WHITE, 'num of queens not replaced -', len(cant_place_indices), 'out of ', N**2)

print(Fore.WHITE, '*****************************************************')
print(Fore.WHITE, 'average success- ', sum(prob) / len(prob))
print(Fore.WHITE, 'min success- ', min(prob))
print(Fore.WHITE, 'max success- ', max(prob))
end = timeit.default_timer()
print(Fore.WHITE, '*****************************************************')
print(Fore.WHITE, 'running time- ', (end - start))
