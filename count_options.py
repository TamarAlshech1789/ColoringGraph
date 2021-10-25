from find_hamilton import *

num_of_options = 0
new_edges = []
N = int(sys.argv[1])
colored_edges = []

def count_options_iterative(colored_edges, all_edges):
    new_color = []
    possible_edges = all_edges.copy()
    for edge in [[0, x] for x in range(1, N+1)]:

def count_options(colored_edges, new_color, all_edges):
    if len(new_color) == N / 2 and not new_color in new_edges:
        new_edges.append(new_color)
        print(new_color)
        return

    else:

        possible_edges = all_edges.copy()

        for edge in all_edges:
            color_OK = 0
            new_color_copy = new_color.copy()
            new_color_copy.append(edge)
            for exist_color in colored_edges:
                if find_small_cycle(N, exist_color, new_color_copy) == True:
                    color_OK += 1

            possible_edges.remove(edge)

            if color_OK == len(colored_edges):
                removed_edges = remove_illegel_edges(N, possible_edges, edge)
                count_options(colored_edges.copy(), new_color_copy.copy(), possible_edges.copy())

            else:
                new_color_copy.remove(edge)

all_edges = list(itertools.combinations(range(N), 2))
color_1 = []
color_2 = []
i = 0
while i < N:
    color_1.append([i, i+1])
    all_edges.remove((i, i+1))
    color_2.append([i+1, (i+2)%N])
    if (i+2)%N == 0:
        all_edges.remove((0, i+1))
    else:
        all_edges.remove((i+1, (i+2)%N))
    i += 2

colored_edges.append(color_1)
colored_edges.append(color_2)
new_color = []

count_options(colored_edges, new_color, all_edges)

print('end!')