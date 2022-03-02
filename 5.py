import numpy as np

flines = open('input_5.txt').read().splitlines()
N = 1000

arr = np.zeros((N,N))

for fline in flines:
    # Read in instructions
    foo, _, foo2 = fline.split(' ')
    x1, y1 = foo.split(',')
    x2, y2 = foo2.split(',')
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # Horizontal
    if x1 == x2:
        if y2 >= y1:
            for y in range(y1, y2+1):
                arr[x1, y] += 1
        else:
            for y in range(y2, y1+1):
                arr[x1, y] += 1
    # Vertical
    elif y1 == y2:
        if x2 >= x1:
            for x in range(x1, x2+1):
                arr[x, y1] += 1
        else:
            for x in range(x2, x1+1):
                arr[x, y1] += 1
    
print(np.sum(arr > 1))

###
# Part two
###
arr = np.zeros((N,N))

for fline in flines:
    # Read in instructions
    foo, _, foo2 = fline.split(' ')
    x1, y1 = foo.split(',')
    x2, y2 = foo2.split(',')
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)

    # Direction vector
    v = np.array([x2 - x1, y2 - y1])
    # Number of steps, single step
    nsteps = max(abs(x2 - x1), abs(y2 - y1))
    dv = [int(vv/nsteps) for vv in v]

    # Fill in the array
    for k in range(nsteps+1):
        arr[x1 + dv[0]*k, y1 + dv[1]*k] += 1

# Number of overlaps
print(np.sum(arr > 1))
