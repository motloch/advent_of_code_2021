import numpy as np
lines = open('input_9.txt').readlines()
lines = [l.replace('\n','') for l in lines]
lines = [[int(x) for x in l] for l in lines]

height = np.array(lines, dtype = int)
N,M = height.shape

# For each point calculate how many of their neighbors are higher
num_higher = np.zeros((N,M))
num_higher[:-1]    += (height[   :-1] >= height[   1:])
num_higher[1:]     += (height[   1:]  >= height[   :-1])
num_higher[:, :-1] += (height[:, :-1] >= height[:, 1:])
num_higher[:, 1:]  += (height[:, 1:]  >= height[:, :-1])

# Lowpoint has no neighbors higher
is_lowpoint = num_higher == 0

# Risk level is height plus one
print(np.sum(is_lowpoint*(height+1)))

###
# Second part
###

# For basins, the only thing that matter is whether height is nine or not
is_top = (height == 9).astype(int)

# Find all basins by a graph search - keep track of which areas have been explored already
# and what are sizes of the basins we found
is_explored = np.zeros((N, M))
basin_sizes = []

# Eventually tries starting a basin search in all areas
for i in range(N):
    for j in range(M):

        # In case we find an area that belongs to an unexplored basin, start the graph
        # search
        if (is_top[i, j] == 1) or is_explored[i, j]:
            continue
        queue = [(i,j)]
        basin_size = 0

        # Continue exploring the current basin
        while len(queue) > 0:
            ci, cj = queue.pop() 
            if not is_explored[ci, cj]:
                is_explored[ci, cj] = True
                basin_size += 1

            # Add the neighbors to the queue if they are part of the same basin
            if ci > 0 and not is_explored[ci - 1, cj] and is_top[ci -1, cj] == 0:
                queue.append((ci - 1, cj))
            if cj > 0 and not is_explored[ci, cj - 1] and is_top[ci, cj -1] == 0:
                queue.append((ci,cj - 1))
            if ci < N-1 and not is_explored[ci + 1, cj] and is_top[ci +1, cj] == 0:
                queue.append((ci + 1, cj))
            if cj < M-1 and not is_explored[ci, cj + 1] and is_top[ci, cj+1] == 0:
                queue.append((ci,cj + 1))

        # Basin exploration finished
        basin_sizes.append(basin_size)

# Product of the sizes of the three largest basins
basin_sizes = np.sort(basin_sizes)
print(basin_sizes[-1]*basin_sizes[-2]*basin_sizes[-3])
