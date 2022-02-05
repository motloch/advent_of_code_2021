import numpy as np

state = open('input_6.txt').readline().replace('\n','').split(',')
state = [int(s) for s in state]

# We will keep track of number of lanternfish of each kind
num_each_kind = np.zeros(9, dtype = int)

for s in state:
    num_each_kind[s] += 1

# Time evolution
for i in range(1, 257):
    new_num_each_kind = np.zeros(9, dtype = int)

    new_num_each_kind[8] = num_each_kind[0]
    new_num_each_kind[6] = num_each_kind[0]
    new_num_each_kind[:8] += num_each_kind[1:]

    num_each_kind = new_num_each_kind

    # Output at desired times
    if i in [80, 256]:
        print(sum(num_each_kind))
