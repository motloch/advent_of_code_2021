import numpy as np
import heapq

# Constant used to represent "unreachable" in Dijkstra's algorithm
MAXDIST = 1e8

# Load input
lines = open('input_15.txt').read().splitlines()

N, M = len(lines), len(lines[0])

dat = np.zeros((N, M), dtype = int)
for i, line in enumerate(lines):
    for j, s in enumerate(line):
        dat[i, j] = int(s)
        
def dijkstra(dat):
    """
    Dijkstra's algorithm on a rectangular lattice with costs of entering each vertex given
    by array "dat".
    
    Prints the minimal cost of path from vertex [0,0] to vertex [-1, -1]
    """
    N, M = dat.shape

    # Optimal distance to any given vertex
    dist = MAXDIST*np.ones((N, M), dtype = int)
    dist[0,0] = 0

    # Keep track of vertices for which we have already found the optimal path
    visited = np.zeros((N, M), dtype = bool)

    # heap with the cost of visited vertices
    pq = []
    heapq.heappush(pq, [0, (0,0)])

    # while we have vertices left in the queue
    while len(pq) > 0:
        # vertex closest to the origin
        v_dist, (x,y) = heapq.heappop(pq)

        # Have we already found the optimal path (was already at the top of the heap)?
        # If so, continue, otherwise add the neighbors to the heap
        if visited[x,y]:
            continue
        else:
            visited[x,y] = True

        # Relative position of the neighbor
        for dx, dy in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
            # Check neighbor exists and we want to still probe it
            if (x + dx >= 0) and (y + dy >= 0) and (x + dx < N) and (y+dy < M):
                if not visited[x+dx, y+dy]:
                    # Add to heap with the proper minimal distance
                    dist[x+dx,y+dy] = min(dist[x+dx,y+dy], dist[x, y] + dat[x+dx, y+dy])
                    heapq.heappush(pq, [dist[x+dx, y+dy], (x+dx, y+dy)])
                    
    print(int(dist[-1,-1]))

dijkstra(dat)

# Part two operates on a bigger array, just copied over 5*5 times
dat2 = np.zeros((5*N, 5*M))
for i in range(5):
    for j in range(5):
        dat2[i*N:(i+1)*N, j*M:(j+1)*M] = 1 + ((dat + i + j - 1) % 9)

dijkstra(dat2)
