import numpy as np

dat = np.loadtxt('input_7.txt', delimiter = ',', dtype = int)
dat = np.sort(dat)

# Optimal position for the first problem is the median
m = np.median(dat)
# This is how much fuel is required
print(np.sum(np.abs(dat - m)))

###
# Second part
###

# Amount of fuel to burn to move x steps
def cost(x):
    return x*(x+1)/2

# Brute force try every possible solution and find the one with minimal fuel consumption
mi = min(dat)
ma = max(dat)
min_cost = 1e12
for i in range(mi, ma+1):
   current_cost = np.sum(cost(np.abs(dat - i)))
   if current_cost < min_cost:
        min_cost = current_cost
    
print(min_cost)
