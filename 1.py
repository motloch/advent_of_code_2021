import numpy as np

dat = np.loadtxt('input_1.txt')

# How many times do the measurements increase?
inc = 0
for i in range(1, 2000):
    if dat[i] > dat[i-1]:
        inc+=1

print(inc)

# Three-measurement sliding window
slide = dat[:-2] + dat[1:-1] + dat[2:]

# How many times does that increase?
inc = 0
for i in range(1, len(slide)):
    if slide[i] > slide[i-1]:
        inc+=1

print(inc)
