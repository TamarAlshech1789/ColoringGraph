import copy

# Python3 program to solve N Queen
# Problem using backtracking
global N
N = 18

global ilegal_conf
ilegal_conf = []

global list_N
list_N = list(range(N))

def printSolution(board):
    for i in range(N):
        for j in range(N):
            print(board[i][j], end=" ")
        print()


# A utility function to check if a queen can
# be placed on board[row][col]. Note that this
# function is called when "col" queens are
# already placed in columns from 0 to col -1.
# So we need to check only left side for
# attacking queens
def isSafe(board, row, col, symbol):
    # Check this col on left side
    for i in range(row):
        if board[i][col] == symbol:
            return False

    # Check left diagonal on upeer side
    for i, j in zip(range(row, -1, -1),
                    range(col, -1, -1)):
        if board[i][j] == symbol:
            return False

    # Check right diagonal on upper side
    for i, j in zip(range(row, -1, -1),
                    range(col, N, 1)):
        if board[i][j] == symbol:
            return False

    return True

def cancelLastStep(board, row, symbol):
    for i in range(N):
        if board[row][i] == symbol:
            board[row][i] = 0
            return

def find_rowAndsymbol(board):
    row = 0
    symbol = 1
    sum_ = (N * (1 + N)) / 2
    for i in range(N-1, -1, -1):
        sum_row = sum(board[i])
        if sum_row > 0:
            row = i
            if sum_row == sum_:
                row += 1
                symbol = 1
            else:
                symbol = max(board[row]) + 1
            break

    return [row, symbol]


def solveNQUtil(board):
    # base case: If all queens are placed
    # then return true

    [row, symbol] = find_rowAndsymbol(board)
    if row >= N:
        return True

    empty_cells  = [index for index, element in enumerate(board[row]) if element == 0]

    # Consider this column and try placing
    # this queen in all rows one by one
    copy_board = copy.deepcopy(board)
    for i in empty_cells:
        if board[row][i] == 0:
            copy_board[row][i] = symbol
            if not copy_board in ilegal_conf and isSafe(board, row, i, symbol):

                # Place this queen in board[i][col]
                board[row][i] = symbol
                # recur to place rest of the queens
                if solveNQUtil(board) == True:
                    return True
                else:
                    while solveNQUtil(board) == False:
                        return False
                    return True

                # If placing queen in board[i][col
                # doesn't lead to a solution, then
                # queen from board[i][col]
            else:
                copy_board[row][i] = 0

    # if the queen can not be placed in any col in
    # this row then return false


    if len(empty_cells) > 0:
        ilegal_conf.append(copy.deepcopy(board))
        if symbol == 1:
            cancelLastStep(board, row - 1, N)
        else:
            cancelLastStep(board, row, symbol - 1)

    return False


# This function solves the N Queen problem using
# Backtracking. It mainly uses solveNQUtil() to
# solve the problem. It returns false if queens
# cannot be placed, otherwise return true and
# placement of queens in the form of 1s.
# note that there may be more than one
# solutions, this function prints one of the
# feasible solutions.
def solveNQ():
    board = [[0 for i in range(N)] for j in range(N)]

    if solveNQUtil(board) == False:
        print("Solution does not exist")
        return False

    printSolution(board)
    return True

for n in [12,14,15,16,18]:
# Driver Code
    N = n
    solveNQ()

# This code is contributed by Divyanshu Mehta