import numpy as np

lines = open('input_4.txt').readlines()

# Read winning numbers
win_nums = lines[0].replace('\n', '').split(',')
win_nums = [int(w) for w in win_nums]

def is_win(a):
    """
    Given a 5*5 array of ones and zeros representing whether a number on a bingo board was
    drawn or not, determine if the board is winning
    """
    for i in range(5):
        if np.sum(a[i]) == 5:
            return True
        if np.sum(a[:,i]) == 5:
            return True
    return False

# For each board, determine on which round it wins and what its score is at that time
win_round = []
scores = []

# Do the calculation
for i in range(100):
    # Load the board, save it as a 2d array
    l1 = lines[2 + 6*i].replace('\n', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')
    l1 = [int(l) for l in l1]                                                  
    l2 = lines[3 + 6*i].replace('\n', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')
    l2 = [int(l) for l in l2]                                                  
    l3 = lines[4 + 6*i].replace('\n', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')
    l3 = [int(l) for l in l3]                                                  
    l4 = lines[5 + 6*i].replace('\n', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')
    l4 = [int(l) for l in l4]                                                  
    l5 = lines[6 + 6*i].replace('\n', '').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').split(' ')
    l5 = [int(l) for l in l5]

    arr = np.zeros((5,5))
    arr[0] = l1
    arr[1] = l2
    arr[2] = l3
    arr[3] = l4
    arr[4] = l5

    # As we go through the drawn numbers one by one, keep track of which fields were hit
    filled = np.zeros((5,5))

    for round_number in range(100):
        # Check if we had winning number in this round
        filled += arr == win_nums[round_number]
        
        # Are we done?
        if is_win(filled):
            win_round.append(round_number)
            score = np.sum(arr*(1 - filled))*win_nums[round_number]
            scores.append(score)
            break
            
print('win first')
print(scores[np.argmin(win_round)])
print('win last')
print(scores[np.argmax(win_round)])
