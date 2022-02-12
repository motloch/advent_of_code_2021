import numpy as np

lines = open('input_10.txt').readlines()
lines = [l.replace('\n', '') for l in lines]

###
# First part
###

score = 0
ranking = {')': 3, ']': 57, '}': 1197, '>': 25137}
is_incomplete = []

for line in lines:
    current = '' # Keep track of the brackets that have not been closed yet
    corrupted = False
    for s in line:
        if not corrupted:
            #Not an end bracket?
            if s in ['[', '(', '<', '{']:
                current += s
            #We start with a closing bracket - corrupted line, add score
            elif len(current) == 0:
                score += ranking[s]
                corrupted = True
            #We finish a bracket
            elif s in [']', ')', '>', '}']:
                #Correctly - closes the bracket
                if (
                    (current[-1] == '[' and s == ']')
                    or
                    (current[-1] == '(' and s == ')')
                    or
                    (current[-1] == '<' and s == '>')
                    or
                    (current[-1] == '{' and s == '}')
                   ):
                    current = current[:-1]
                #Incorrectly - corrupted line, add score
                else:
                    score += ranking[s]
                    corrupted = True

    # Keep track of which lines are incomplete for the second part
    if corrupted:
        is_incomplete.append(False) 
    else:
        is_incomplete.append(True)

print(score)

###
# Second part
###

scores = []
ranking = {'(': 1, '[': 2, '{': 3, '<': 4}

for i, line in enumerate(lines):
    if not is_incomplete[i]:
        continue

    current = ''
    for s in line:
        #Not an end bracket?
        if s in ['[', '(', '<', '{']:
            current += s
        #We finish a bracket
        elif s in [']', ')', '>', '}']:
            #Correctly
            if (
                (current[-1] == '[' and s == ']')
                or
                (current[-1] == '(' and s == ')')
                or
                (current[-1] == '<' and s == '>')
                or
                (current[-1] == '{' and s == '}')
               ):
                current = current[:-1]
            #We should have filtered out the corrupted lines by now
            else:
                print('Error on line ', line)

    #At this point current contains a list of unclosed brackets, such as '[(<'

    # Flipt the order for ease of calculation and calculate score
    current = current[::-1]
    current_score = 0
    for s in current:
        current_score *= 5
        current_score += ranking[s]
    scores.append(current_score)

print(np.median(scores))
