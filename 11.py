import numpy as np

# Load an array of digits
arr = open('input_11.txt').read().splitlines()
arr = [[int(y) for y in x] for x in arr]
arr = np.array(arr, dtype = int)
N = len(arr)

# Set of vectors to all neighbors
dd = [[dx, dy] for dx in [-1, 0, 1] for dy in [-1, 0, 1]]

def step(arr):
    """
    Given an N*N array with digits representing the energy levels of individual octopuses,
    returns
    a) number of flashes in the next step
    b) energy levels of these octopuses after the step
    """

    num_flashes = 0

    # Increase the energy level of each octopus
    arr += 1

    # Keep track of who flashed - each can only flash once
    flashed = np.zeros((N,N), dtype = int)

    # Keep track of which octopuses flashed at the current stage of the "propagation
    # avalanche"
    current_flash = (arr > 9)*(1 - flashed)

    # As long as the flash is propagating around, continue
    while np.sum(current_flash) > 0:
        
        # Remember the octopuses that flashed, reset their energy level
        flashed += current_flash
        arr *= 1-current_flash

        # Update number of flashes
        num_flashes += np.sum(current_flash)

        # Propagate to the neighbors
        for i in range(N):
            for j in range(N):
                if current_flash[i,j]:
                    for dx,dy in dd:
                        # Check bounds
                        if i + dx >= 0 and i + dx < N and j + dy >= 0 and j + dy < N:
                            # Make sure no one flashes twice in the same step
                            if not flashed[i+dx, j+dy]:
                                arr[i+dx, j+dy] += 1

        # Check if there are octopuses that flash because of an irradiation by a neighbor
        current_flash = (arr > 9)*(1 - flashed)

    return num_flashes, arr

# Simulate the time evolution of the system
total_flashes = 0

for i in range(500):
    n, arr = step(arr)
    total_flashes += n

    # First problem - how many flashes after 100 steps?
    if i == 99:
        print(total_flashes)

    # Second problem - when do all the octopuses flash simultaneously?
    if n == N**2:
        print(i+1)
        exit()

