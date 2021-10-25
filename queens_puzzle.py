''' Python3 program to solve N Queen Problem using
backtracking '''
import itertools
import sys
import timeit
from termcolor import colored

result = []

# A utility function to print solution


''' A utility function to check if a queen can
be placed on board[row][col]. Note that this
function is called when "col" queens are
already placed in columns from 0 to col -1.
So we need to check only left side for
attacking queens '''


def isSafe(board, row, col):
    # Check this row on left side
    for i in range(col):
        if (board[row][i]):
            return False

    # Check upper diagonal on left side
    i = row
    j = col
    while i >= 0 and j >= 0:
        if (board[i][j]):
            return False
        i -= 1
        j -= 1

    # Check lower diagonal on left side
    i = row
    j = col
    while j >= 0 and i < n:
        if (board[i][j]):
            return False
        i = i + 1
        j = j - 1

    return True


''' A recursive utility function to solve N
Queen problem '''


def solveNQUtil(board, col):
    ''' base case: If all queens are placed
    then return true '''
    if (col == n):
        v = []
        for i in board:
            for j in range(len(i)):
                if i[j] == 1:
                    v.append(j + 1)
        result.append(v)
        return True

    ''' Consider this column and try placing
    this queen in all rows one by one '''
    res = False
    for i in range(n):

        ''' Check if queen can be placed on
        board[i][col] '''
        if (isSafe(board, i, col)):
            # Place this queen in board[i][col]
            board[i][col] = 1

            # Make result true if any placement
            # is possible
            res = solveNQUtil(board, col + 1) or res

            ''' If placing queen in board[i][col]
            doesn't lead to a solution, then
            remove queen from board[i][col] '''
            board[i][col] = 0  # BACKTRACK

    ''' If queen can not be place in any row in
        this column col then return false '''
    return res


''' This function solves the N Queen problem using
Backtracking. It mainly uses solveNQUtil() to
solve the problem. It returns false if queens
cannot be placed, otherwise return true and
prints placement of queens in the form of 1s.
Please note that there may be more than one
solutions, this function prints one of the
feasible solutions.'''


def solveNQ(n):
    result.clear()
    board = [[0 for j in range(n)]
             for i in range(n)]
    solveNQUtil(board, 0)
    result.sort()
    return result


def check_royal_latin_square(board, n, mismatches):
    r = range(n)
    check_valididy = True
    for (x1,x2) in itertools.combinations(r, 2):
        queen1, queen2 = board[x1], board[x2]

        if (queen2 - queen1)%n == x2 - x1:
            check_valididy = False
            mismatches.append([x1,x2, '+'])
        elif (queen2 - queen1)%n == (x1 - x2)%n:
            check_valididy = False
            mismatches.append([x1, x2, '-'])
    return check_valididy, mismatches

def print_row(queen, n):
    str = ''
    for i in range(n):
        if i == (queen - 1):
            str += '  *  '
        else:
            str += '  -  '
    print (str)

def print_res(res, n):
    board_num = 0
    total_board_num = 0
    for board in res:
        mismatches = []
        validity, mismatches = check_royal_latin_square(board, n, mismatches)
        if validity == False:

            board_num += 1
            print('board number: ', board_num)
            for queen in board:
                print_row(queen, n)

            print('queens mismatches - ', mismatches)

            print()
        total_board_num += 1

    print('-------------------------------------')
    print('number of validity queens placements - ', (total_board_num - board_num), ' / ', total_board_num)

def check_first_match(queens, q):
    for queen in queens:
        if queen[0] == q:
            return False
    return True

def check_queens(queens, n):
    board = [[0 for i in range(n)] for j in range(n)]

    for queen in queens:
        for i, q in enumerate(queen):
            if board[i][q-1] == 1:
                return False
            board[i][q-1] = 1
    return True

def print_borad(queens, n):
    board = [[0 for i in range(n)] for i in range(n)]
    j = 1
    for queen in queens:
        for row in range(n):
            board[row][queen[row] - 1] = j
        j+= 1
    for row in range(n):
        str = ''
        for i in range(n):
            str += '  %s  ' %board[row][i]
        print(str)
    print()


def check_not_cyclic(queens, n):
    for j in range(len(queens)-1):
        queen1, queen2 = queens[j], queens[j + 1]
        diff = (queen2[0] - queen1[0]) % n
        for i in range(1,n):
            if not (queen2[i] - queen1[i]) % n == diff:
                return True
    return False

def merge_queens(res, n):
    for queens_indexs in itertools.combinations(range(len(res)), n):
        queens = []
        good_match = True
        for i in queens_indexs:
            if check_first_match(queens, res[i][0]) == False:
                good_match = False
                pass
            else:
                queens.append(res[i])

        if good_match == True:
            if check_queens(queens, n) == True:
                if check_not_cyclic(queens, n) == True:
                    print(queens)

def create_all_option(queens, n):
    all_options = [[queen] for queen in queens[0]]
    for i in range(1, n):
        new_all_options = []
        for op in all_options:
            for queen in queens[i]:
                new_op = op.copy()
                new_op.append(queen)

                if check_queens(new_op, n) == True:
                    new_all_options.append(new_op)

        all_options = new_all_options.copy()

    return all_options

def merge_ordered_queens(queens, n, not_cyclic=False):
    queens_options = create_all_option(queens, n)
    for i, queens in enumerate(queens_options):
        print('--------- solution num. ', i + 1, ' ----------')
        print_borad(queens, n)
        if not_cyclic == True and check_not_cyclic(queens, n) == True:
            print(colored('not cyclic!!', 'red'))
        print('----------------------------------')
        print()

def order_queens(res, n):
    queens = [[] for i in range(n)]
    for queen in res:
        queens[queen[0] - 1].append(queen)

    return queens

# Driver Code

def print_queens(queens, n):
    for row in range(n):
        str_row = ''
        for col in range(n):
            if col == (queens[row] - 1):
                str_row += '  Q  '
            else:
                str_row += '  -  '
        print(str_row)


#command = sys.argv[1]
command = 'print_queens'
n = 11
start = timeit.default_timer()
res = solveNQ(n)

if command == 'print_queens':
    place = [0 for i in range(n)]
    for i, r in enumerate(res):
        if r[0] == 1:
            print('************ solution num. ', i + 1, ' ************')
            print_queens(r, n)
            place[r[0] - 1] += 1
    print('*****************************************************')
    for i,p in enumerate(place):
        print('number of ', i, 's: ', p)
else:
    if command == 'uncyclic':
        if len(res) < n:
            print('not enough queens placements!')
        else:
            res = order_queens(res, n)
            merge_ordered_queens(res, n, not_cyclic = True)
    else:
        res = order_queens(res, n)
        merge_ordered_queens(res, n)

stop = timeit.default_timer()
print('runtime - ', stop - start)

# This code is contributed by YatinGupta