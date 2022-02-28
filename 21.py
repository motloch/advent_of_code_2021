import numpy as np

# Whether we are using the example, or the problem
test = False

# Starting positions of the two players
if test:
    p1 = 4
    p2 = 8
else:
    p1 = 1
    p2 = 5

# Scores
WINNING_SCORE = 1000
s1 = 0
s2 = 0

# Current state of the dice (on the first roll we have to get one)
d = 100

def roll(d):
    """
    Roll once when the state of the dice is d. Return the result.
    """
    return 1 + (d % 100)

def triple_roll(d):
    """
    Roll three times when the state of the dice is d. Return the sum and the final state
    of the dice
    """
    res = 0
    for i in range(3):
        d = roll(d)
        res += d
    return res, d

# Keep track of how many times we rolled the dice
roll_no = 0

# Play the game until someone wins
while (s1 < WINNING_SCORE) and (s2 < WINNING_SCORE):

    # Player one rolls three times
    r1, d = triple_roll(d) 
    roll_no += 3
    # Their position is updated
    p1 = 1 + ((p1+r1 - 1) % 10)
    # Their score is updated
    s1 += p1
    # Check for win
    if s1 >= WINNING_SCORE:
        print(s2*roll_no)
        continue

    # The same for second player
    r2, d = triple_roll(d) 
    roll_no += 3
    p2 = 1 + ((p2+r2 - 1) % 10)
    s2 += p2
    if s2 >= WINNING_SCORE:
        print(s1*roll_no)
        continue

###
# Second problem
###

# Starting positions
if test:
    p1 = 4
    p2 = 8
else:
    p1 = 1
    p2 = 5

# Keep track of the number of universes in which each player wins
w1 = 0
w2 = 0

# Array with results of a single roll of a three-sided dice
dice = np.array([1,2,3])
# Array with results (sums) of rolling a three-sided dice three times (with repetition)
dice3 = (dice[None,None,:] + dice[None,:,None] + dice[:,None,None]).flatten()

# Build a dictionary that for each possible result of a roll of three dice (3, 4,
# .., 9) counts how many times it can happen.
dices = {i:0 for i in range(3,10)}
for d in dice3:
    dices[d] += 1

# All that pracitally matters is at each point keeping track of the number of Universes at
# given:
#   p1 position, p2 position, p1 score, p2 score
# We store these in an array that is rather small, because we only have to keep track of
# these numbers for Universes where none of the players have won yet
state = np.zeros((11, 11, 21, 21), dtype = int)

# at the beginning the position is deterministic - there is only a single Universe and we
# know player's position exactly
state[p1, p2, 0, 0] = 1

# Repat while we have a Universe where one of the players has not won yet
while np.sum(state) > 0:
    
    # Player one's turn
    new_state = np.zeros((11, 11, 21, 21))

    # Iterate over all possible player one positions and scores
    for p1 in range(1,11):
        for s1 in range(21):
            
            # Iterate over all possible dice results
            for d in dices:
                # New player one position in the corresponding Universe
                new_p1 = 1 + ((p1+d - 1) % 10)

                # Does player one win?
                if s1 + new_p1 >= 21:
                    # Increase the win number counter. The total number of wins is equal
                    # to product of starting number of Universes and number of dice roll
                    # combinations that give d. Notice that player 2 position/score does
                    # not matter, so we sum over them.
                    w1 += np.sum(state[p1, :, s1, :])*dices[d]
                else:
                    # We get to a Universe with player one having higher score
                    new_state[new_p1, :, s1+new_p1, :] += state[p1, :, s1, :]*dices[d]
    state = new_state

    # Player two's turn - the same logic
    new_state = np.zeros((11, 11, 21, 21))
    for p2 in range(1,11):
        for s2 in range(21):
            for d in dices:
                new_p2 = 1 + ((p2+d - 1) % 10)
                if s2 + new_p2 >= 21:
                    w2 += np.sum(state[:, p2, :, s2])*dices[d]
                else:
                    new_state[:, new_p2, :, s2+new_p2] += state[:, p2, :, s2]*dices[d]
    state = new_state

# Find in how many Universes does the winning player win
print(int(max(w1, w2)))
