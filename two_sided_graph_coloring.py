import sys
import itertools
import timeit

def good_color(N, colors, color2):
    for color1 in colors:
        first_v = 0
        curr_v = color2.index(color1[first_v])
        cycle_len = 2
        while not curr_v == first_v:
            curr_v = color2.index(color1[curr_v])
            cycle_len += 2

        if cycle_len < 2 * N:
            return False
    return True


def legal_permutation(N, p):
    for i, e in enumerate(p):
        if i == e or i == (e - 1)%N:
            return False
    return True

N = int(sys.argv[1])

permutations = list(itertools.permutations(range(N)))

color1 = tuple(range(N))
color2 = tuple([i%N for i in range(1,N +1)])
colors = [color1, color2]

permutations.remove(color1)
permutations.remove(color2)

good_p = []
for p in permutations:
    if legal_permutation(N, p) == True:
        if good_color(N, colors, p) == True:
            good_p.append(p)

print('n: ', N)
print('*****************************************************')
print("number of ways to color the third color: ", len(good_p))

#find 4-th color
start = timeit.default_timer()
num_of_4_color = 0
color4 = [[] for i in good_p]
good_p_4 = good_p.copy()
curr_num_of_4_color = [0 for i in good_p]
for i, color3 in enumerate(good_p):
    colors.append(color3)
    good_p_4.remove(color3)
    for p in good_p_4:
        if good_color(N, colors, p) == True:
            curr_num_of_4_color[i] += 1
            if not (p in good_p and p[0] < color3[0]):
                num_of_4_color += 1
                color4[i].append(p)
    good_p_4.append(color3)
    colors.remove(color3)

    #print('3-color: ', color3, ', number of 4-color: ', curr_num_of_4_color)

end = timeit.default_timer()
#print('run time: ', end - start)
print('*****************************************************')
print('all options for 4-th color: ', num_of_4_color)
print('*****************************************************')

options = []
for count in curr_num_of_4_color:
    if not count in options:
        options.append(count)
        print('number of 3-color with *', count, '* options for 4-color: ', curr_num_of_4_color.count(count))