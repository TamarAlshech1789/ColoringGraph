import sys
import random
import numpy as np

'''
input: size N of board
output: placement of max number of queens in NxN chessboard 
        that will not threaten each other using random-greedy
'''
def queens_place(N):
    rows = list(range(N))
    cols = list(range(N))
    queensRows = []
    queensCols = []
    queensDiagDown = []
    queensDiagUp = []

    FailedLotteries = 0

    while FailedLotteries < len(rows) * len(cols):
        row = random.choice(rows)
        col = random.choice(cols)

        FailedLotteries = FailedLotteries + 1

        diagUp = row - col
        diagDown = row + col
        if(not diagUp in queensDiagUp and not diagDown in queensDiagDown):
            FailedLotteries = 0
            queensRows.append(row)
            queensCols.append(col)
            queensDiagUp.append(diagUp)
            queensDiagDown.append(diagDown)
            rows.remove(row)
            cols.remove(col)

    print('Number of Queens: ', len(queensRows))
    matrix = [['-' for i in range(N)] for j in range(N)]
    for i in range(len(queensRows)):
        matrix[queensRows[i]][queensCols[i]] = '*'

    str = ''
    for row in range(N):
        for col in range(N):
            str = str + matrix[row][col]
            if(col < N-1):
                str = str + ', '
        print(str)
        str = ''

'''
input: size N of board
output: placement of max number of queens in NxN chessboard 
        that will not threaten each other using random-greedy
'''
def color_graph(N):
    adjency_matrix = np.identity(N) - np.ones(N)
    nodes = list(range(N))
    colors = list(range(1, N ))
    number_edges = 0
    while True:
        if number_edges == (pow(N, 2) - N) / 2:
            print('all edges are colored!')
            break
        x = np.random.choice(nodes)
        nodes.remove(x)
        y = np.random.choice(nodes)
        nodes.append(x)
        '''here we can prove our running time by not choosing couples we already chose:'''
        if adjency_matrix[x, y] > 0:
            continue

        for n in nodes:
            if adjency_matrix[x, n] in colors :
                colors.remove(adjency_matrix[x, n])
            if adjency_matrix[n, y] in colors:
                colors.remove(adjency_matrix[n, y])

        if len(colors) == 0:
            print('number of edges not colored: ', int((pow(N, 2) - N) / 2) - number_edges)
            break
        else:
            adjency_matrix[x,y] = adjency_matrix[y, x] = random.choice(colors)
            number_edges += 1
            colors = list(range(1, N + 1))

if __name__ == '__main__':
    problem = sys.argv[1]
    N = int(sys.argv[2])
    if problem == 'Queens':
        queens_place(N)
    elif problem == 'Graph':
        for i in range(10):
            color_graph(N)
    
