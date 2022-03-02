# Store the state as a string - the first seven characters represent the hallways where
# the amphipods can stop (not front of a room), then we have the first room, second room,
# etc. We designate empty place with '.'
# We use a recursion and keep track of optimal scores for each state we have already
# encountered, to avoid recomputations.

from math import ceil, floor

###
### Constants
###

NUM_HW = 7 # Number of hallways where the amphipods can stop (not front of the room)

###
### Read input, initialize
###

lines = open('input_23_second.txt').read().splitlines()

N = len(lines) - 3 #length of a room

initial = '.' * NUM_HW # Construct the initial state
for col in range(4):
    for row in range(N):
        initial += lines[2+row][3 + 2*col].lower()

unit_cost = {'a': 1, 'b': 10, 'c': 100, 'd': 1000} # Movement costs

requested_state = '.'*NUM_HW + 'a'*N + 'b'*N + 'c'*N + 'd'*N # This is the final state


###
### Useful routines
###

def get_room(state, room_no):
    """
    Get a string representing the current state of the room
    """
    return state[NUM_HW + N*room_no:NUM_HW + N*room_no + N]

def is_room_accepting(state, room_no):
    """
    Determine if the room is ready to accept amphipods (i.e. no "foreign" amphipods are
    present and there is still empty space)
    """
    inhabitant = chr(97 + room_no)
    room = get_room(state, room_no)

    # We are done with this room
    if room == inhabitant*N:
        return False

    # Remove the empty space, if present
    room = room.replace('.', '')

    # Check if any amphipods not belonging here are present
    if room == inhabitant*len(room):
        return True

    return False

def is_room_empty(state, room_no):
    """
    Determine if the room is completely empty
    """
    room = get_room(state, room_no)

    return room == '.'*N

def no_one_wants_out(state, room_no):
    """
    Determine if the room is filled with the amphipods that live there
    """
    room = get_room(state, room_no)
    requested_inhabitant = chr(97 + room_no)
    want_elsewhere = room.replace('.','').replace(requested_inhabitant, '')

    return  want_elsewhere == ''

def top_amphipod(state, room_no):
    """
    Find the character of the amphipod at the top of the room
    """
    room = get_room(state, room_no)

    # Remove the empty space, if present
    room = room.replace('.', '')

    if room == '':
        print('No top amphipod, room empty!')
        exit()

    return room[0]

def position_for_taking(state, room_no):
    """
    Find the top ampiphod in the room and return the index of its position in the state
    string
    """
    room = get_room(state, room_no)

    pos = 0

    while room[pos] == '.' and pos < N:
        pos += 1

    if pos == N:
        print('Taking from an empty room!')
        exit()

    return NUM_HW + N*room_no + pos

def position_for_putting(state, room_no):
    """
    Find the top-most empty positon in the room and return the index of this position in
    the state string
    """
    room = get_room(state, room_no)

    pos = 0

    while pos < N and room[pos] == '.':
        pos += 1

    if pos == 0:
        print('Putting into a full room!')
        exit()

    return NUM_HW + N*room_no + pos - 1

def hw_pos_to_xy(hw_pos):
    """
    Convert hallway position to xy
    """
    if hw_pos == 0:
        return [0,0]
    if hw_pos == 1:
        return [1,0]
    if hw_pos == 2:
        return [3,0]
    if hw_pos == 3:
        return [5,0]
    if hw_pos == 4:
        return [7,0]
    if hw_pos == 5:
        return [9,0]
    if hw_pos == 6:
        return [10,0]

def rm_pos_to_xy(rm_pos):
    """
    Convert room position to xy
    """
    pos = rm_pos - NUM_HW
    rm_no = pos // N
    rm_pos = pos % N
    return [2 + 2*rm_no, 1 + rm_pos]

def pos_to_xy(pos):
    """
    Convert position to xy
    """
    if pos < NUM_HW: # Hallway
        return hw_pos_to_xy(pos)
    else: # Room
        return rm_pos_to_xy(pos)

def dist(old_pos, new_pos):
    """
    Given two positions as indexed in the state string, return a number of steps between the two
    """

    x0,y0 = pos_to_xy(old_pos)
    x1,y1 = pos_to_xy(new_pos)

    return abs(x0 - x1) + y0 + y1

def can_travel(state, from_pos, to_pos):
    """
    Given a string representing the state and positions from and to (rooms are placed at
    positions 1.5, 2.5, 3.5 and 4.5), return a boolean telling us whether we can go
    between these positions at the moment.
    """

    # Check if origin/destination are rooms
    going_from_room = from_pos - int(from_pos) != 0
    going_to_room = to_pos - int(to_pos) != 0

    # the positions in between have indices in range [a, b] with a < b
    if from_pos > to_pos:
        if going_to_room:
            a = ceil(to_pos)
        else:
            a = to_pos

        if going_from_room:
            b = floor(from_pos)
        else:
            b = from_pos - 1
    else:
        if going_from_room:
            a = ceil(from_pos)
        else:
            a = from_pos + 1

        if going_to_room:
            b = floor(to_pos)
        else:
            b = to_pos

    # Take the string representing places we have to go through and check if they are
    # empty
    hs = state[a:b+1].replace('.', '')

    return hs == ''

def can_get_from_hw_to_room(state, hallway_no, room_no):
    """
    Given a string representing the state, return a boolean telling us whether we can go
    between from given hallway position to given room.
    """
    return can_travel(state, hallway_no, room_no + 1.5)

def list_rm_acessible_from_hw(state, hallway_no):
    """
    Given a state, return a list of rooms currently acessible from the given hallway
    """
    out = []

    for room_no in range(4):
        if can_travel(state[:NUM_HW], 1.5 + room_no, hallway_no):
            out.append(room_no)

    return out
    
def get_new_state(state, move_from, move_to):
    """
    Perform a move and return the new state
    """
    s = list(state) 
    s[move_to] = s[move_from]
    s[move_from] = '.'
    return ''.join(s)

###
### Solve the problem by recursion, while keeping track of the situations we have already
### encountered
###

best_solutions = {}

def find_optimal_solution(state):
    """
    Return the cost of going from given state to the final state. If we did not
    investigate this state before, save the result into best_solutions.
    """
    
    # Avoid duplicit calculations
    if state in best_solutions:
        return best_solutions[state]

    # We are done
    if state == requested_state:
        return 0
    
    # If we can get an amphipod home, do it as that is always optimal. Only do hallway ->
    # room, as room -> room can be constructed from two moves.
    for room_no in range(4):
        if is_room_accepting(state, room_no):
            requested_inhabitant = chr(97 + room_no)

            for hallway_no in range(NUM_HW):
                # Check if we have the correct amphipod and we can travel
                if not can_get_from_hw_to_room(state[:NUM_HW], hallway_no, room_no):
                    continue
                is_correct_amphipod = state[hallway_no] == requested_inhabitant

                # If we can, get a new state, calculate the cost and return
                if is_correct_amphipod:
                    new_pos = position_for_putting(state, room_no)
                    new_state = get_new_state(state, hallway_no, new_pos)
                    if new_state in best_solutions:
                        cost = best_solutions[new_state]
                    else:
                        cost = find_optimal_solution(new_state)
                    cost += unit_cost[requested_inhabitant] * dist(new_pos, hallway_no)
                    best_solutions[state] = cost
                    return cost

    # Otherwise we have to find the optimal move room -> hallway
    min_cost = 1e9

    # Moves room -> hallway
    # Cycle through all empty hallways and rooms acessible from them
    for hallway_no in range(NUM_HW):
        if state[hallway_no] == '.':
            rm_acessible = list_rm_acessible_from_hw(state, hallway_no)
            for room_no in rm_acessible:
                # Check we can move out of the room
                if is_room_empty(state, room_no):
                    continue
                if no_one_wants_out(state, room_no):
                    continue

                # Try the move, keeping track of the minimal cost solution
                inhabitant = top_amphipod(state, room_no)
                old_pos = position_for_taking(state, room_no)
                new_state = get_new_state(state, old_pos, hallway_no)
                if new_state in best_solutions:
                    cost = best_solutions[new_state]
                else:
                    cost = find_optimal_solution(new_state)
                cost += unit_cost[inhabitant] * dist(old_pos, hallway_no)
                if cost < min_cost:
                    min_cost = cost
    
    # Save the new result for later reuse
    best_solutions[state] = min_cost
    return min_cost

find_optimal_solution(initial)

print(best_solutions[initial])
