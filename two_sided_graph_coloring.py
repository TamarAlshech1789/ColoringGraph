import sys
import itertools

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

print("number of ways to color the third color: ", len(good_p))


