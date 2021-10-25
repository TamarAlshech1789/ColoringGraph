import sys
import itertools
import numpy as np
import math

def printLatin(n):
    # A variable to control the
    # rotation point.
    k = n + 1

    # Loop to prrows
    for i in range(1, n + 1, 1):

        # This loops runs only after first
        # iteration of outer loop. It prints
        # numbers from n to k
        temp = k
        while (temp <= n):
            print(temp, end=" ")
            temp += 1

        # This loop prints numbers
        # from 1 to k-1.
        for j in range(1, k):
            print(j, end=" ")

        k -= 1
        print()

def check_if_ls(ls):
    for row in ls:
        l = list(range(n))
        for r in row:
            if r in l:
                l.remove(r)
            else:
                return False
    ls = np.array(ls)
    for col in ls.T:
        l = list(range(n))
        for c in col:
            if c in l:
                l.remove(c)
            else:
                return False

    print(ls)
    return True

def find_diagonal_ls(n):
    set = range(n)
    per = list(itertools.permutations(set))

    #split
    split_per = [[] for i in set]
    for p in per:
        for i in set:
            if p[i] == i:
                split_per[i].append(list(p))

    count_ls = 0
    for p1 in split_per[0]:
        for p2 in split_per[1]:
            for p3 in split_per[2]:
                for p4 in split_per[3]:
                    for p5 in split_per[4]:
                        if check_if_ls([p1,p2,p3,p4,p5]) == True:
                            count_ls+=1
                            print('another one! num. ', count_ls)

n = int(sys.argv[1])
find_diagonal_ls(n)

