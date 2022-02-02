import numpy as np

lines = open('input_3.txt').readlines()
L = 12 # Number of bits
N = len(lines)

# Number of ones at L-th position
num_1 = np.zeros(L, dtype = int)
# Number of zeros at L-th position
num_0 = np.zeros(L, dtype = int)

# Count number of ones/zeros
for line in lines:
    for i in range(L):
        if line[i] == '1':
            num_1[i] += 1
        else:
            num_0[i] += 1

# Calculate gamma - first as a string in binary
g = ''
for i in range(L):
    if num_1[i] > num_0[i]:
        g += '1'
    else:
        g += '0'
gg = int(g, 2)

# Calculate epsilon - first as a string in binary
e = ''
for i in range(L):
    if num_1[i] < num_0[i]:
        e += '1'
    else:
        e += '0'
ee = int(e, 2)

print(ee*gg)

####
# Second problem
####

oxygen_list = []
for line in lines:
    oxygen_list.append(line[:-1])

for j in range(L):
    # find maximal bit
    num_1 = 0
    num_0 = 0
    for element in oxygen_list:
        if element[j] == '1':
            num_1 += 1
        if element[j] == '0':
            num_0 += 1

    #Ties go towards ones
    to_keep = '1'
    if num_0 > num_1:
        to_keep = '0'

    #remove the other guys
    remains = []
    for element in oxygen_list:
        if element[j] == to_keep:
            remains.append(element)

    oxygen_list = remains

ox = remains[0]

co2_list = []
for line in lines:
    co2_list.append(line[:-1])

for j in range(L):
    # find maximal bit
    num_1 = 0
    num_0 = 0
    for element in co2_list:
        if element[j] == '1':
            num_1 += 1
        if element[j] == '0':
            num_0 += 1

    #Ties go towards zeros
    to_keep = '0'
    if num_0 > num_1:
        to_keep = '1'

    #remove the other guys
    remains = []
    for element in co2_list:
        if element[j] == to_keep:
            remains.append(element)

    co2_list = remains
    if len(co2_list) == 1:
        break

co2 = remains[0]
print(int(ox, 2)*int(co2, 2))
