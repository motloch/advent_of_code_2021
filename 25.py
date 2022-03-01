import numpy as np

# Read in the input file
lines = [l.replace('\n', '') for l in open('input_25.txt').readlines()]

# Size of the array
N,M = len(lines), len(lines[0])

# Convert the input into an array of zeros (nothing), ones (downward cucumber) and twos
# (rightward cucumber)
arr = np.zeros((N,M), dtype = int)
for i, line in enumerate(lines):
    for j, s in enumerate(line):
        if s == '.':
            arr[i,j] = 0
        elif s == 'v':
            arr[i,j] = 2
        elif s == '>':
            arr[i,j] = 1
        else:
            print('problem')

# Keep track if any cucumber moved in the current step and the number of steps
moved = True
num_steps = 0

# Repeat as long as things move
while moved:

    # Initialize new iteration
    num_steps += 1
    moved = False

    # This will be the situation after the move
    new_arr = np.zeros((N,M), dtype = int)

    #Move the eastward ones.
    for i in range(N):
        for j in range(M):
            if arr[i, j] == 0: #empty space
                continue
            elif arr[i, j] == 2: #downward cucumber
                new_arr[i,j] = 2
            else:
                newj = (j + 1) % M    # new position if it moves (wraps around)
                if arr[i, newj] == 0: # we can move
                    moved = True
                    new_arr[i,newj] = arr[i,j]
                else:               # we can not move
                    new_arr[i,j] = arr[i,j]

    arr = new_arr
    new_arr = np.zeros((N, M), dtype = int)

    #Move the southward ones
    for i in range(N):
        for j in range(M):
            if arr[i,j] == 0: #empty space
                continue
            elif arr[i,j] == 1: #downward cucumber
                new_arr[i,j] = 1
            else:
                newi = (i + 1) % N # new position if it moves (wraps around)
                if arr[newi, j] == 0: # we can move
                    moved = True
                    new_arr[newi,j] = arr[i,j]
                else:               # we can not move
                    new_arr[i,j] = arr[i,j]
    arr = new_arr

print(num_steps)
