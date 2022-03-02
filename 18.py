import re

def explode(s):
    """
    Take a string representing a snail number and return 
    1) a string representing a snail number after one explosion (if exists)
    2) whether explosion happened
    """

    # Find if there is a pair nested inside four pairs by comparing number of opened
    # brackets
    current_count = 0
    found = False
    for i, ss in enumerate(s):
        if ss == '[':
            current_count += 1
        if ss == ']':
            current_count -= 1
        # If we find five opened brackets at any time, we are done
        if current_count == 5:
            found = True
            break
            
    # No explosion is possible
    if not found:
        return s, False
    # Explosion is possible 
    else:
        # b includes everything up to the opening "[" of the pair we are exploding
        #(i tells us where the explosion happens)
        b = s[:i]
        #n1, n2 are the numbers from the pair we are exploding, a is the remainder
        n1, n2, a = re.search('\[(\d+),(\d+)\](.*)', s[i:]).groups()
        n1 = int(n1)
        n2 = int(n2)

        # find the first regular number to the left (if any)
        b_regex = re.search('(.*[^\d]+)(\d+)([^\d]+)', b)
        # find the first regular number to the right (if any)
        a_regex = re.search('([^\d]+)(\d+)([^\d]+.*)', a)

        # if there is a regular number to the left, add n1 to it. Keep the parts before
        # and after the number intact
        if b_regex is not None:
            bb, bn, ba = b_regex.groups()
            bn = str(int(bn) + n1)
            b = bb + bn + ba
        # same with the right and adding n2
        if a_regex is not None:
            ab, an, aa = a_regex.groups()
            an = str(int(an) + n2)
            a = ab + an + aa

        # return resulted exploded number
        return b + '0' + a, True

def split(s):
    """
    Take a string representing a snail number and return 
    1) a string representing a snail number after one split (if exists)
    2) whether split happened
    """

    # We split snail numbers where any number is 10 or greater = two or more digits next
    # to each other
    e_regex = re.search('(\d\d+)', s)

    # If no such number present, we are done
    if e_regex is None:
        return s, False
    # Otherwise split
    else:
        # Part left of the number to split
        b = s[:e_regex.start()]
        # Number to split
        m = int(s[e_regex.start():e_regex.end()])
        # How it splits
        m1 = m//2
        m2 = m - m1
        # Part right of the number to split
        a = s[e_regex.end():]

        return b + '[' + str(m1) + ',' + str(m2) + ']' + a, True

def add(s1, s2):
    """
    Return result of addition of two snail numbers encoded as strings. Return a string,
    after performing all the explosions and splits
    """

    #Naive addition
    s = '[' + s1 + ',' + s2 + ']'

    #While we explode or split, continue
    cont = True
    while cont:
        # First try if there is an explosion
        s, expl = explode(s)
        # If there is not, try a split
        if not expl:
            s, spl = split(s)

        # If there is no explosion or split, we are done
        if (not expl) and (not spl):
            cont = False

    return s

def magnitude(s):
    """
    Return magnitude of a snail number encoded as a string. Return an integer.
    """
    # Magnitude of a number is the number itself
    if '[' not in s:
        return int(s)
    # We have a snail number [s1,s2]
    else:
        # find the split between the s1 and s2 by keeping track of how many more [ than ]
        # we have encountered when reading the string from the left. When the difference
        # is equal to one, we know we reached the comma between s1 and s2
        current_count = 0
        for i, ss in enumerate(s):
            if ss == '[':
                current_count += 1
            if ss == ']':
                current_count -= 1
            if current_count == 1 and i > 0:
                break

        # Left and right elements (omit the leftmost [, rightmost ] and the dividing
        # comma)
        s1 = s[1:i+1]
        s2 = s[i+2:-1]

        return 3*magnitude(s1) + 2*magnitude(s2) 

###
# Problem 1
###

# Load input
lines = open('input_18.txt').read().splitlines()

# Perform addition of all numbers from the input and return the magnitude of the result
s = lines[0]
for line in lines[1:]:
    s = add(s, line)
print(magnitude(s))

###
# Problem 2
###

# What is the largest magnitude you can get from adding only two of the snailfish numbers?

N = len(lines)
max_sum = -1

# Try all pairs and keep track of the maximal achieved sum
for i in range(N):
    for j in range(N):
        if i == j:
            continue
        s = add(lines[i], lines[j])
        current_sum = magnitude(s)
        if current_sum > max_sum:
            max_sum = current_sum

print(max_sum)
