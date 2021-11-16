import numpy as np
import random

global _lanbda
_lambda = 10**3

global N
N = 10

global num_rotations
num_rotations = 10**7

global marked_cells
marked_cells = [0]
from colorama import Fore

global board
board = np.zeros(N**2).reshape((N, N))

global indices
indices = list(np.ndindex(board.shape))

def print_solution():
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                print(Fore.RED, '--', end=" ")
            else:
                print(Fore.WHITE, "{:02d}".format(int(board[i][j])), end=" ")
        print()

#find all possible symbol for a single cell
def find_possible_symbols(cell):
    symbols = list(range(1, N+1))
    (row, col) = cell

    for r in range(N):
        if not r == row and board[r][col] in symbols :
            symbols.remove(board[r][col])
    for c in range(N):
        if not c == col and board[row][c] in symbols:
            symbols.remove(board[row][c])

    # Check left diagonal on upeer side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    # Check left diagonal on lower side
    for i, j in zip(range(row, N, 1),
                    range(col, -1, -1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, -1, -1),
                    range(col, N, 1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    # Check right diagonal on upper side
    for i, j in zip(range(row, N, 1),
                    range(col, N, 1)):
        if board[i][j] in symbols:
            symbols.remove(board[i][j])

    symbols.append(0)
    return symbols

def get_probability(symbols, symbol, board_cell):
    sum_lambda = 0
    curr_lambda = 0
    exponent = marked_cells[0]

    for s in symbols:
        add = 0
        if s == 0:
            if board_cell == 0:
                add = _lambda ** (exponent)
            else:
                add = _lambda ** (exponent - 1)
            if s == symbol:
                curr_lambda = add
        else:
            if board_cell == 0:
                add = _lambda ** (exponent + 1)
            else:
                add = _lambda ** (exponent)
            if s == symbol:
                curr_lambda = add
        sum_lambda += add

    return curr_lambda / sum_lambda

def metropolis_RLS():
    keep_placing = 0
    while(keep_placing < num_rotations):
        cell = random.choice(indices)
        possible_symbols = find_possible_symbols(cell)
        symbol = random.choice(possible_symbols)
        p = get_probability(possible_symbols, symbol, board[cell[0]][cell[1]])
        update = np.random.choice([0,1], 1, p=[1 - p, p])

        if update == 1:
            if board[cell[0]][cell[1]] == 0 and symbol > 0:
                marked_cells[0] += 1
            if board[cell[0]][cell[1]] > 0 and symbol == 0:
                marked_cells[0] -= 1
            board[cell[0]][cell[1]] = symbol

        keep_placing += 1



#define initial legal board
for i in range(N):
    board[i][i] = i + 1
marked_cells[0] = N
metropolis_RLS()
print('number of placements -', marked_cells[0])
print_solution()
