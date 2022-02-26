import numpy as np

# Input
lines = open('input_20.txt').readlines()
lines = [l.replace('\n', '') for l in lines]

# image enhancement algorithm as array of ones and zeros
# 0 = dark pixel, 1 = light pixel
conversion = lines[0].replace('.', '0').replace('#', '1')
conversion = [int(s) for s in conversion]

# starting input image as array of strings
# size of the input image
field = lines[2:]
N = len(field)
M = len(field[0])

# convert input image into 2D array of zeros and ones
# 0 = dark pixel, 1 = light pixel
arr = np.zeros((N, M), dtype = int)
for i, line in enumerate(field):
    for j, s in enumerate(line):
        if s == '.':
            arr[i, j] = 0
        else:
            arr[i, j] = 1

# What is outside the probed area (dark pixels)
outside = 0

def remap(arr):
    """
    Given nine pixels from the image as a 3*3 array of ones and zeros, return pixel of the
    output image by indexing into the proper part of the image enhancement algorithm array
    """
    # Nine pixels -> index in the image enhancement algorithm encoding
    num = np.sum(arr*[[256,128,64],[32,16,8],[4,2,1]])

    return conversion[num]

def make_output(arr, outside):
    """
    Given a 2D array of ones and zeros representing the currently known map of the trench
    and a zero or one representing whether the pixels outside are dark or light, return
    the next iteration of the map.
    """
    # Current size of the map
    N, M = arr.shape

    # For the processing we need a slightly bigger input map, because the 2D kernel
    # reaches outside of the arr bounds. We thus create a bigger array, fill the middle
    # part with currently known map of the trench and the outside with dark or light
    # pixels, whatever our current knowledge of them is
    arr2 = outside*np.ones((N+6, M+6), dtype = int)
    arr2[3:-3, 3:-3] = arr

    # We go through the array in a straightforward way and figure out the pixel outputs
    # after an iteration
    out = np.zeros((N+4, M+4), dtype = int)
    for i in range(N+4):
        for j in range(M+4):
            out[i,j] = remap(arr2[i:i+3, j:j+3])

    # Pixels outside of the mapped regions correpond to either [[0,0,0],[0,0,0],[0,0,0]]
    # or the same with ones. Their mappings are straightforward
    if outside == 0:
        outside = conversion[0]
    else:
        outside = conversion[-1]

    # Return the (extended) mapped region and information about the outside pixels
    return out, outside

# Return number of light pixels after 2 and 50 iterations
for i in range(50):
    arr, outside = make_output(arr, outside)
    if i in [1, 49]:
        print(np.sum(arr))
