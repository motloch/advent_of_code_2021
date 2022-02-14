import numpy as np

fname = 'input_13.txt'
mr = 820 # Number of dots

# Load the positions of the dots
dat = np.loadtxt(fname, max_rows = mr, delimiter = ',', dtype = int)

# Size of the paper
N = np.max(dat[:,1]) + 1
M = np.max(dat[:,0]) + 1

# Fill in 2D array with positions of the dots
arr = np.zeros((N, M), dtype = bool)
for x, y in dat:
    arr[y, x] = True

def fold_up(arr, a):
    """
    Takes in an array with the positions of the dots and where to fold it. Returns an
    array representing the paper with the dots after an "up" fold.
    """
    N = arr.shape[0]
    
    arr[N - 2*a-1:N-a-1] += arr[-1:N-a-1:-1]
    return arr[N-2*a-1:N-a-1]

def fold_left(arr, a):
    """
    Takes in an array with the positions of the dots and where to fold it. Returns an
    array representing the paper with the dots after a "left" fold.
    """
    M = arr.shape[1]
    
    arr[:,M - 2*a-1:M-a-1] += arr[:,-1:M-a-1:-1]
    return arr[:,M-2*a-1:M-a-1]

# Read the folding instructions and perform them on the array with the dot positions
lines = open(fname).readlines()[mr+1:]
for line in lines:
    _, _, instr = line.replace('\n', '').split(' ')
    d, a = instr.split('=')
    a = int(a)

    # Perform the fold
    if d == 'y':
        arr = fold_up(arr, a)
    else:
        arr = fold_left(arr, a)

    # Print number of visible dots after the first fold
    if a == 655:
        print(np.sum(arr))

# Print how the resulting piece of paper looks like
for a in arr:
    print(''.join([str(int(x)) for x in a]))
