# The program can be split into repeated call 
#   z = f(z, a, b, c, input)
# where the function f is schematically written as
# def f(z, a, b, c, input):
#   x = input != ((z % 26) + b)
#   return (z//a)*(25*x + 1) + x*(input + c)
#
# From studying the input, we see that
#  * a is either 1 or 26, each appears seven times
#  * b is always >= 10 when a == 1, always negative when a == 26
#  * c is always positive, ranging between 4 and 15
#
# Because of these constraints, we can think of the computation as performing operations
# on a base 26 number z: 
# If x evaluates to False, then z either does not change (if a == 1) or we discard the
# last digit of z and shift the digits to the right (if a == 26).
# If x evaluates to True, then the last digit is set to input + c (always non-negative,
# smaller than 26) and the other digits are set to all digits of z at the moment (a == 1)
# or all digits of z at the moment except for the last one, that is discarded (a == 26)
#
# Because b is always positive when a == 1, each such function evaluation necessarily
# (because input can not be equal to (z%26) + b and so x is one) increases the number of
# digits. This happens seven times, which means the other seven times we _must_ decrease
# the number of digits to end up with zero. This means that when a == 26, we need to have
# input equal to (z%26) + b, i.e. b plus the currently last digit of z.

NINST = 14

# Read lines with instructions
lines = [l.replace('\n', '') for l in open('input_24.txt').readlines()]
# Separate them into instructions that encode the function f
instr = [lines[18*i:18*(i+1)] for i in range(NINST)]

def read_abc(i):
    """
    Given a list of instructions (as strings), return values of a, b and c (see the
    function definition at the very beginning). Also check the other instructions are as
    they should be.

    Return a list of three integers.
    """

    # Read off the values of a, b, c
    abc = []
    abc.append(int(i[4][6:]))
    abc.append(int(i[5][6:]))
    abc.append(int(i[15][6:]))

    # Check the instructions are in the form we claim they are
    wrong = False
    if i[0] != 'inp w': wrong = True
    if i[1] != 'mul x 0': wrong = True
    if i[2] != 'add x z': wrong = True
    if i[3] != 'mod x 26': wrong = True
    if i[4][:6] != 'div z ': wrong = True
    if i[5][:6] != 'add x ': wrong = True
    if i[6] != 'eql x w': wrong = True
    if i[7] != 'eql x 0': wrong = True
    if i[8] != 'mul y 0': wrong = True
    if i[9] != 'add y 25': wrong = True
    if i[10] != 'mul y x': wrong = True
    if i[11] != 'add y 1': wrong = True
    if i[12] != 'mul z y': wrong = True
    if i[13] != 'mul y 0': wrong = True
    if i[14] != 'add y w': wrong = True
    if i[15][:6] != 'add y ': wrong = True
    if i[16] != 'mul y x': wrong = True
    if i[17] != 'add z y': wrong = True

    if wrong:
        print('Instructions corrupted!')
        exit()
    else:
        return abc
    
# Get values of a,b,c for all function calls
all_abc = []
for i in range(NINST):
    all_abc.append(read_abc(instr[i]))

# Let's assume the the input digits are I_1, I_2, ... and simulate the calculation. As we
# know, at each point each digit of z is some I_i + c_i. We will thus keep track of the
# indexes i that correspond to the first, second, ... digit of z at the moment.
#
# If at given step
#   a == 1, then we have to extend z. We do it by appending i
#   a == 26, then we have to shrink z to achieve z == 0 in the end. This means we need
#               I_i == I_j + c_j + b_i
#            where j is the last digit of z at the moment.

# For post-processing, we keep track of (i, j, c_j + b_i)
for_processing = []

# Number z at the moment, represented by indices of I_i + c_i that form the digits of z
z = []

# Process the algorithm
for i in range(NINST):
    a,b,c = all_abc[i]
    # We extend z
    if a == 1:
        z.append(i)
    # We must shrink, keep track of which input digits are related and how
    elif a == 26:
        j = z.pop()
        c_j = all_abc[j][2]
        for_processing.append([i, j, c_j + b])

###
# First problem - largest accepted number
###
out = [0 for i in range(NINST)]

# We know which input digits are related and how, so maximize the larger one and set it to
# nine
for i, j, cj_plus_bi in for_processing:
    if cj_plus_bi > 0:
        # I_i is bigger
        out[i] = str(9)
        out[j] = str(9 - cj_plus_bi)
    else:
        # I_j is bigger
        out[j] = str(9)
        out[i] = str(9 + cj_plus_bi)

print(''.join(out))

###
# Second problem - smallest accepted number
###
out = [0 for i in range(NINST)]

# We know which input digits are related and how, so maximize the larger one and set it to
# nine
for i, j, cj_plus_bi in for_processing:
    if cj_plus_bi > 0:
        # I_i is bigger
        out[i] = str(1 + cj_plus_bi)
        out[j] = str(1)
    else:
        # I_j is bigger
        out[j] = str(1 - cj_plus_bi)
        out[i] = str(1)

print(''.join(out))
