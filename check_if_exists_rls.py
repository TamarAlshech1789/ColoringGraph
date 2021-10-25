import sys
from itertools import permutations

def check_single_ls(ls, rows, cols):
    for col in range(cols):
        l = list(range(cols))
        for row in range(rows):
            if not ls[row][col] in l:
                return False
            l.remove(ls[row][col])
    return True

def check_diagonal(ls, rows, cols):
    for row in range(rows):
        for col in range(cols):
            symbol = ls[row][col]
            # Check upper diagonal on left side
            i = row
            j = col
            while i >= 0 and j >= 0:
                if (ls[i][j] == symbol and not (i == row and  j == col)):
                    return False
                i -= 1
                j -= 1

            i = row
            j = col
            while i >= 0 and j < cols:
                if (ls[i][j] == symbol and not (i == row and  j == col)):
                    return False
                i -= 1
                j += 1

            i = row
            j = col
            while i < rows  and j >= 0:
                if (ls[i][j] == symbol and not (i == row and  j == col)):
                    return False
                i += 1
                j -= 1

            # Check lower diagonal on left side
            i = row
            j = col
            while j >= 0 and i < rows:
                if (ls[i][j] == symbol and not (i == row and  j == col)):
                    return False
                i = i + 1
                j = j - 1
    return True

def create_all_ls(elements, n, number):
    success = False
    per = list(permutations(range(1, n ), n - 1))
    for p in per:
        ls = [elements[0]]
        for i in range(n - 1):
            ls.append(elements[p[i]])
        if check_single_ls(ls, n, n) and check_diagonal(ls, n, n):
            for i in range(n):
                print(ls[i])
            print('success!')
            number += 1
            print()
    return number

n = int(sys.argv[1])
# this will create all permutations of length 3 of [0,1,2]
orders = list(permutations(range(n), n))
orders_mat = [[] for i in range(n)]
order_0 = orders[0]
for order in orders:
    orders_mat[order[0]].append(order)
    #if order[0] == 0:
        #orders.remove(order)

m = len(orders_mat[0])
i_0 = 0
number = 0
"""
for order_1 in orders:
    ls = [order_0, order_1]
    if(check_single_ls(ls, 2, n) and check_diagonal(ls, 2, n)) == False:
        continue
    for order_2 in orders:
        ls = [order_0, order_1, order_2]
        if not check_single_ls(ls, 3, n) and check_diagonal(ls, 3, n):
            continue
        for order_3 in orders:
            ls = [order_0, order_1, order_2, order_3]
            if not check_single_ls(ls, 4, n) and check_diagonal(ls, 4, n):
                continue
            for order_4 in orders:
                ls = [order_0, order_1, order_2, order_3, order_4]
                if not check_single_ls(ls, 5, n) and check_diagonal(ls, 5, n):
                    continue
                for order_5 in orders:
                    ls = [order_0, order_1, order_2, order_3, order_4, order_5]
                    if check_single_ls(ls, 6, n) and check_diagonal(ls, 6, n):
                        print('success!')
                        number += 1
                        for i in range(n):
                            print(ls[i])
                        print()
"""
for i_1 in range(m):
    for i_2 in range(m):
        for i_3 in range(m):
            elements = [orders_mat[0][i_0], orders_mat[1][i_1], orders_mat[2][i_2], orders_mat[3][i_3]]
            number = create_all_ls(elements, n, number)
            """for i_4 in range(m):
                
                if orders_mat[1][i_1] == (1,2,3,4,0) and orders_mat[2][i_2] == (2,3,4,0,1) and orders_mat[3][i_3] == (3,4,0,1,2) and orders_mat[4][i_4]==(4,0,1,2,3):
                    print('here!')
                elements = [orders_mat[0][i_0], orders_mat[1][i_1], orders_mat[2][i_2], orders_mat[3][i_3], orders_mat[4][i_4]]
                number =  create_all_ls(elements, n, number)
                
                for i_5 in range(m):
                    elements = [orders_mat[0][i_0], orders_mat[1][i_1], orders_mat[2][i_2], orders_mat[3][i_3], orders_mat[4][i_4], orders_mat[5][i_5]]
                    number =  create_all_ls(elements, n, number)
                
                    for i_6 in range(m):
                        elements = [orders_mat[0][i_0], orders_mat[1][i_1], orders_mat[2][i_2], orders_mat[3][i_3],
                                    orders_mat[4][i_4], orders_mat[5][i_5], orders_mat[6][i_6]]
                        number = create_all_ls(elements, n, number)
                    """
print('number of options: ', number)

