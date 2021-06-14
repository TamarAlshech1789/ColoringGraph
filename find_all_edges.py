from find_hamilton import *

def same_vertices(edges):
    vertices = []
    for edge in edges:
        ver1 = edge[0]
        ver2 = edge[1]
        if ver1 in vertices or ver2 in vertices:
            return False

        vertices.append(ver1)
        vertices.append(ver2)

    return True

def print_option(options):
    curr_first_edge = options[0][0]
    num_edges = 0
    for op in options:
        if op[0] == curr_first_edge:
            num_edges += 1
        else:
            print('first edge: ', curr_first_edge, ', number of options: ', num_edges)
            num_edges = 1
            curr_first_edge = op[0]
    print('first edge: ', curr_first_edge, ', number of options: ', num_edges)

def find_edges(colored_edges, possible_edges):
    color_option = [[edge] for edge in possible_edges]
    finished = False

    while(finished == False):
        finished = True
        temp_color_option = []
        for option in color_option:
            for edge in possible_edges:
                if not edge in option:
                    new_option = option.copy()
                    new_option.append(edge)
                    new_option.sort()

                    if not new_option in temp_color_option and same_vertices(new_option):
                        no_small_cycles = 0
                        for exist_color in colored_edges:
                            if find_small_cycle(N, exist_color, new_option) == True:
                                no_small_cycles += 1

                        if no_small_cycles == len(colored_edges):
                            temp_color_option.append(new_option)
                            if len(new_option) < (N/2):
                                finished = False
        color_option = temp_color_option.copy()

    print('number of option: ', len(color_option))
    print_option(color_option)


N = int(sys.argv[1])

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

colored_edges = []
colored_edges.append(color_1)
colored_edges.append(color_2)

find_edges(colored_edges, all_edges)