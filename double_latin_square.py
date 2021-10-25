import sys
import numpy as np

def check_curr_column(new_color_column, color_columns, counter):
    for i, column in enumerate(color_columns):
        if counter - i == abs(new_color_column - column):
            return False

    return True

def check_color(i, j, p, q, alpha, beta, square, color):
    color_columns = []
    counter = 0
    for x_i in range(p):
        for x_j in range(q):
            color_column = ((alpha * x_i + i) % p ) * q + (beta * x_j + j) % q

            if color_column in color_columns:
                print('not latin square for alphha = ', alpha, ' , beta = ', beta)
                return []

            if check_curr_column(color_column, color_columns, counter) == False:
                print('error in diagonal! alphha = ', alpha, ' , beta = ', beta, ' , color = ', color)
                return []

            color_columns.append(color_column)
            counter += 1

            if x_i * q + x_j >= p * q or color_column >= p * q:
                print('error!')

            square[x_i * q + x_j][color_column] = color

    return square

def check_alpha_beta(p, q, alpha, beta, square):
    color = 0
    for i in range(p):
        for j in range(q):
            square = check_color(i, j, p, q, alpha, beta, square, color)
            if square == []:
                return False
            color += 1
    return True

def check_latin_square(square, n):
    for row in square:
        for i in range(n):
            if not i in row:
                return False
    square_T = np.array(square).T.tolist()
    for col in square_T:
        for i in range(n):
            if not i in col:
                return False

    return True


def computeGCD(x, y):
    if x > y:
        small = y
    else:
        small = x
    for i in range(1, small + 1):
        if ((x % i == 0) and (y % i == 0)):
            gcd = i

    return gcd

p = int(sys.argv[1])
q = int(sys.argv[2])
#alpha = int(sys.argv[3])
#beta = int(sys.argv[4])

for alpha in range(1, p):
    for beta in range(1 , q):
        if computeGCD(alpha, p ) == 1 and computeGCD(beta, q) == 1:
            square = [[-1 for i in range(p*q)] for j in range(p*q)]

            #check_alpha_beta(p, q, alpha, beta, square) == True
            if check_alpha_beta(p, q, alpha, beta, square) == True:
                print('good for alphha = ', alpha, ' , beta = ', beta)
                #for row in square:
            #    print(row)
