import sys
import random
import itertools

def find_next_edge_in_path(v, edges):
    for i, edge in enumerate(edges):
        if v in edge:
            if v == edge[0]:
                v = edge[1]
            else:
                v = edge[0]
            return edge, v

    return [], -1


def find_small_cycle(N, color_1, color_2):
    new_color = color_2.copy()
    for edge in new_color:
        new_color.remove(edge)
        first_v = edge[0]
        curr_v = edge[1]
        path_len = 1
        end_path = False

        while end_path == False:
            if path_len%2 == 1:
                [next_edge, curr_v] = find_next_edge_in_path(curr_v, color_1)
            else:
                [next_edge, curr_v] = find_next_edge_in_path(curr_v, new_color)

            if len(next_edge) == 0:
                end_path = True
            else:
                path_len += 1

                if path_len == N:
                    return True

                if path_len%2 == 1:
                    new_color.remove(next_edge)

                if first_v in next_edge:
                    return False

                edge = next_edge

    return True

def add_edge(N, colored_edges, new_edges, edge):
    if edge in new_edges:
        return False
    new_edges.append(edge)

    for color in colored_edges:
        if edge in color:
            return False

    for color in colored_edges:
        if find_small_cycle(N, color, new_edges.copy()) == False:
            return False

    return True

def remove_illegel_edges(N, all_edges, edge):
    possible_edges = all_edges.copy()
    v1, v2 = edge[0], edge[1]
    for i in range(N):
        if (v1, i) in possible_edges:
            possible_edges.remove((v1, i))
        if (i, v1) in possible_edges:
            possible_edges.remove((i, v1))

        if (i, v2) in possible_edges:
            possible_edges.remove((i, v2))
        if (v2, i) in possible_edges:
            possible_edges.remove((v2, i))

    return possible_edges

def add_single_hamilton(N, colored_edges, new_edges):
    all_edges = list(itertools.combinations(range(N), 2))
    possible_edges = all_edges.copy()
    good_edges = all_edges.copy()
    while len(new_edges) < (N / 2):
        if len(possible_edges) == 0:
            if len(new_edges) == 0:
                print ("No hamilton cycles to add!")
                return False
            if len(good_edges) == 1:
                new_edges = new_edges[:-2]
                good_edges = all_edges.copy()
            else:
                good_edges.remove(tuple(new_edges[-1]))
                new_edges = new_edges[:-1]
            possible_edges = good_edges.copy()

        edge = random.choice(possible_edges)
        possible_edges.remove(edge)
        edge = list(edge)

        detached_edge = True
        for e in new_edges:
            if edge[0] in e or edge[1] in e:
                detached_edge = False
        if detached_edge == True and add_edge(N, colored_edges, new_edges.copy(), edge) == True:
            new_edges.append(edge)
            remove_illegel_edges(N, possible_edges, edge)
            good_edges = all_edges.copy()

    return True
if __name__ == '__main__':
    N = int(sys.argv[1])

    colored_edges = []
    color_1 = []
    color_2 = []
    i = 0
    while i < N:
        color_1.append([i, i+1])
        color_2.append([i+1, (i+2)%N])
        i += 2

    colored_edges.append(color_1)
    colored_edges.append(color_2)

    #new = [[1, 8], [3, 7], [2, 9], [0, 5], [4, 6]]
    #add_single_hamilton(N, colored_edges, new)
    #colored_edges.append(new)

    #new_color = []
    #while(True):
    #    new_color = []
    #    add_single_hamilton(N, colored_edges, new_color)

    new_color = []
    if add_single_hamilton(N, colored_edges, new_color) == True:
        print("found another hamilton cycle!")
        print(new_color)

    colored_edges.append(new_color)
    new_color = []
    if add_single_hamilton(N, colored_edges, new_color) == True:
        print("found another hamilton cycle!")
        print(new_color)