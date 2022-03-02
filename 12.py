lines = open('input_12.txt').read().splitlines()

#Read in the graph as a dictionary - for each vertex save the neighbors as a list
graph = {}

for line in lines:
    a, b = line.split('-')
    for f, t in [[a,b], [b,a]]:
        if f in graph:
            graph[f].append(t)
        else:
            graph[f] = [t]

#First problem - how many paths 'start' - 'end' are there if we can visit vertices
#starting with a lowercase letter max once?
def count_paths_from(path_so_far):
    """
    Given a path in the graph, use recursion to calculate number of paths from the vertex
    where we have ended (so far) to the vertex called 'end'. If we are in the 'end' vertex
    already, return number 1.
    """
    current_vertex = path_so_far[-1]

    if current_vertex == 'end':
        return 1

    # Recursion over the neighbors
    result = 0
    for v in graph[current_vertex]:
        # We can only visit vertices starting with lowercase letter once
        if (v not in path_so_far) or v[0].isupper():
            result += count_paths_from(path_so_far + [v])

    return result

print(count_paths_from(['start']))

#Second problem - how many paths 'start' - 'end' are there if we can visit a single vertex
#starting with a lowercase letter twice and all other vertices starting with a lowercase
#letter max once?

def count_revisit_paths_from(path_so_far):
    """
    Given a path in the graph, use recursion to calculate number of paths from the vertex
    where we have ended (so far) to the vertex called 'end'. If we are in the 'end' vertex
    already, return number 1. Unlike the function above, we are allowed to visit a single
    vertex starting with a lowercase letter twice.
    """
    current = path_so_far[-1]

    if current == 'end':
        return 1

    # Check if we have already visitied any of the vertices twice
    double_visit = False
    for i in range(len(path_so_far)):
        if (path_so_far[i].islower()) and (path_so_far[i] in path_so_far[i+1:]):
            double_visit = True

    # Recursion over the neighbors
    result = 0
    for v in graph[current]:
        # We can not return to start
        if v == 'start':
            continue

        # Check whether we can enter this neighbor and if so, recurse
        previously_visited = v in path_so_far
        can_we_enter = v.isupper() or (not previously_visited) or (not double_visit)
        if can_we_enter:
            result += count_revisit_paths_from(path_so_far + [v])

    return result

print(count_revisit_paths_from(['start']))
