# The basic idea of this solution is that given two beacons at (bx, by, bz) and (Bx, By,
# Bz), then a vector V defined as follows:
#   d = (abs(bx - Bx), abs(by - By), abs(bz - Bz))
#   V = ( min(d), median(d), max(d) )
# does not change when we shift the coordinate axes, perform 90 degree rotations or
# mirroring. In other words, if two scanners both detect these two beacons, they find the
# same vector of V. We will call V "invariant distance".
#
# To utilize this, for each scanner we calculate V for each pair of beacons the scanner
# sees. By comparing lists of V between scanners, we will be able to figure out which
# beacons are seen by both scanners.
#
# Once we know these mappings, it is straightforward to find the coordinate tranformation
# between the two scanners.

import numpy as np
from copy import deepcopy

# Read the input textfile
lines = open('input_19.txt').readlines()
lines = [l.replace('\n', '') for l in lines]

# Figure out on which lines in the file the scanners start
scanners_starts = [i for i in range(len(lines)) if 'scanner' in lines[i]]

# Number of scanners
N = len(scanners_starts)

# Read in beacon locations in the original coordinate systems of each scanner: construct
# a dictionary where keys are scanner numbers (integers) and values are (nbeacons,
# 3)-sized arrays with beacon coordinates
beacons_orig = {}
for scanner_no in range(N):
    # Lines with beacon locations for this particular scanner
    if scanner_no < N - 1:
        txt = lines[scanners_starts[scanner_no]+1:scanners_starts[scanner_no+1]-1]
    else:
        txt = lines[scanners_starts[-1]+1:]

    # Convert locations of the beacons into a 2D array
    n = len(txt)
    arr = np.zeros((n, 3), dtype = int)
    for i in range(n):
        n1, n2, n3 = txt[i].split(',')
        arr[i] = [int(n1), int(n2), int(n3)]

    beacons_orig[scanner_no] = arr

# Number of beacons seen by each scanner
n_beacons = {k:len(beacons_orig[k]) for k in beacons_orig}

def get_invariant_diffs(i):
    """
    For scanner #i, return an array of "invariant differences" and beacon numbers for each
    pair of beacons (vector of length five for each pair).

    The "invariant differences" are vectors defined at the beginning.

    For future speedup, return the output array sorted by the x, y and z coordinates
    """
    # Only interested in beacons of this particular scanner
    beacons = beacons_orig[i]

    out = []

    # Cycle over pairs, calculate "invariant differences" and store beacon info
    for n1 in range(len(beacons)):
        for n2 in range(n1+1, len(beacons)):
            diff = beacons[n1] - beacons[n2]
            d123 = np.sort(np.abs(diff))
            out.append([*d123, n1, n2])

    # Sort
    out = np.array(out)
    idx = np.lexsort((out[:,2], out[:,1], out[:,0]))
    out = out[idx]

    return out

# Precompute invariant differences for all scanners (and remember which beacons those are)
diffs = [get_invariant_diffs(i) for i in range(N)]

def bigger(x, y):
    """
    Given two vectors, decide if vector x is bigger than y by first comparing the first
    component, in case of a draw the second component and finally the third component, if
    necessary
    """
    if x[0] > y[0]:
        return True
    if x[0] < y[0]:
        return False
    # Only gets here if x0 == y0
    if x[1] > y[1]:
        return True
    if x[1] < y[1]:
        return False
    # Only gets here if x0 == y0 and x1 == y1
    if x[2] > y[2]:
        return True
    if x[2] < y[2]:
        return False
    return False

def equal(x, y):
    """
    Given two vectors, decide if they are identical
    """
    return sum((x-y)**2) == 0

def vector_to_int(v):
    """
    Takes a vector with integer coordinates between -2000 and 2000 and converts it into an
    integer in a reversible manner. Used for hashing.
    """
    if abs(v[0]) > 2000 or abs(v[1]) > 2000 or abs(v[2]) > 2000:
        print('wrong vector to int', v)
        exit()

    return (v[0] + 2000)*5000**2 + (v[1]+2000)*5000 + (v[2]+2000)

# All 48 matrices that can represent relative scanner orientations
from itertools import permutations, combinations_with_replacement
axes = list(permutations([0, 1, 2]))
signs = [[(-1)**a, (-1)**b, (-1)**c] for a in [0,1] for b in [0,1] for c in [0,1]]
Ms = []
for a in axes:
    for s in signs:
        M = np.zeros((3,3))
        for i, j in enumerate(a):
            M[i,j] = s[i]
        Ms.append(M)

def get_matches(s0, s1):
    """
    Find all invariant difference matches between the two scanners s0 and s1. 
    
    Return a dictionary where the key is the hash of the "invariant difference" and the
    value is a list where the first value is a list of corresponding beacon indices of
    scanner s0 and the second value is a list of corresponding beacon indices of s1.
    """

    # Invariant differences and beacon numbers for all pairs of beacons from the two
    # scanners
    diff0 = diffs[s0]
    diff1 = diffs[s1]

    matches = {}

    # Because the lists of invariant differences are sorted, a single pass is enough
    pair_i1 = 0

    # Search counterparts for each beacon pair from the first scanner
    for pair_i0 in range(len(diff0)):
        
        # We do not have to go back to earlier pairs from s1, because of presorting.
        # Go through the pairs from s1 as long as the pair of the first scanner has bigger
        # invariant difference
        while pair_i1 < len(diff1) and bigger(diff0[pair_i0, :3], diff1[pair_i1, :3]):
            pair_i1 += 1

        # Avoid array overshoot
        if pair_i1 > len(diff1) - 1:
            pair_i1 -= 1

        # Do we have a match?
        if equal(diff0[pair_i0, :3], diff1[pair_i1, :3]):
            # Hash value
            h = vector_to_int(diff0[pair_i1,:3])
            # Keep track of the corresponding beacons from both scanners. 
            if h in matches:
                # No need to consider having two pairs with the same invariant distance
                # for the input file we have.
                print('Double counting pairs!')
                exit()
            else:
                new_v = set(diff0[pair_i0,3:])
                new_w = set(diff1[pair_i1,3:])
                matches[h] = [new_v, new_w]

    return matches

def get_mappings(s0, s1, matches):
    """
    Given two scanners s0 and s1 and a dictionary of the form
        hash of invariant difference: [ 
                                        [corresponding vertices from s0],
                                        [corresponding vertices from s1]
                                      ]
    where we only include invariant differences common to both scanners, calculate
    dictionary of the form
        beacon index in s0: beacon index in s1
    for the beacons that are uniquely determined.
    """
    # Numbers of beacons for each scanner
    n0 = n_beacons[s0]
    n1 = n_beacons[s1]

    # Keep track of which beacons from the s1 can correspond to each of the beacons from
    # the s0. At the beginning, they all can.
    all_set = set((i for i in range(n1)))
    mapping = {i:all_set for i in range(n0)}

    # Given the correspondence between the pairs of points, restrict the possible
    # mappings
    for k in matches:
        vs,ws = matches[k]
        for v in vs:
            mapping[v] = mapping[v] & ws

    # Only return a dictionary with mappings that we know for sure (there is only a single
    # beacon remaining)
    mapping_final = {}
    for i in range(n0):
        if len(mapping[i]) == 0:
            print('Inconsistent mappings!')
            exit()
        elif len(mapping[i]) == 1:
                mapping_final[i] = min(mapping[i])

    return mapping_final

shifts_and_rotations = []
for s0 in range(N):
    for s1 in range(s0+1,N):

        matches = get_matches(s0, s1)

        # At this point we assume that for any pair of beacons (A,B) and (C,D) from
        # two different scanners that are separated by the same invariant difference, the
        # beacons (A,B) correspond to either (C,D) or (D,C). If this is not true, we are
        # overly restrictive, which can mean we lose a solution.

        if len(matches) >= 12:

            mapping_final = get_mappings(s0, s1, matches)
                
            # Do we have enough information for this pair of scanners?
            if len(mapping_final) >= 12:

                # Positions of beacons in the original coordinate frames of the scanners
                xyz0 = []
                xyz1 = []
                for k in mapping_final:
                    xyz0.append(beacons_orig[s0][k])
                    xyz1.append(beacons_orig[s1][mapping_final[k]])
                xyz0 = np.array(xyz0)
                xyz1 = np.array(xyz1)

                # Try all rotations/mirrorings and pick the correct one
                for M in Ms:
                    shift = xyz0 - np.dot(xyz1,M)
                    # Minimal and maximal shift in each direction
                    min_shift = np.min(shift, axis = 0)
                    max_shift = np.max(shift, axis = 0)
                    # Are they the same? Then we have a pure translation between the two
                    # and we found the correct rotation
                    if equal(max_shift, min_shift):
                        shifts_and_rotations.append([s0, s1, shift[0], M])
                        break

# For each scanner, find a shift and rotation matrix relative to the coordinate system of
# the first scanner. Keep track of the results in a dictionary.
relative_to_zero = {0: [np.zeros(3), np.eye(3)]}

# For which scanners we know shift and rotation relative to the scanner zero
resolved = np.zeros(N, dtype = bool)
resolved[0] = True

# Repeat until we know shift and rotation for all scanners
while sum(resolved) < N:
    for s0, s1, shift, M in shifts_and_rotations:
        # The convention above is
        #   (coordinates of s0) = shift + (coordinates of s1)*M

        if (resolved[s0] and not resolved[s1]):
            # In the first case we know how to go from s0 to the first scanner. Now we
            # know how to go from s1 to s0, 
            #   (coordinates of first scanner) = shift0 + (coordinates of s0)*M0 ,
            # so we can combine the two 
            shift0 = relative_to_zero[s0][0]
            M0 = relative_to_zero[s0][1]

            new_M = np.dot(M, M0)
            new_shift = shift0 + np.dot(shift, M0)
            relative_to_zero[s1] = [new_shift, new_M]
            resolved[s1] = True
        elif (resolved[s1] and not resolved[s0]):
            # This is analogous, we only have to express s1 coordinates in terms of s0
            # coordinates, which is straightforward
            shift1 = relative_to_zero[s1][0]
            M1 = relative_to_zero[s1][1]

            Minv = np.linalg.inv(M)
            new_M = np.dot(Minv, M1)
            new_shift = shift1 - np.dot(np.dot(shift,Minv), M1)
            relative_to_zero[s0] = [new_shift, new_M]
            resolved[s0] = True

# These are positions of all beacons in the coordinate system of the first scanner.
# Duplicates allowed.
all_beacons = []
for scanner_no in range(N):
    for beacon in beacons_orig[scanner_no]:
        new_pos = relative_to_zero[scanner_no][0] + np.dot(beacon, relative_to_zero[scanner_no][1])
        all_beacons.append(new_pos)

# Sort the beacon positions
all_beacons = np.array(all_beacons)
idx = np.lexsort((all_beacons[:,2], all_beacons[:,1], all_beacons[:,0]))
all_beacons = all_beacons[idx]

# Pick up only the unique beacons
unique_beacons = [all_beacons[0]]
for i in range(1,len(all_beacons)):
    if sum((all_beacons[i] - all_beacons[i-1])**2) != 0:
        unique_beacons.append(all_beacons[i])

print(len(unique_beacons))

###
# Problem 2
###

# Scanner positions are relative_to_zero[i][0], so we can easily go through all pairs
max_dist = 0
for i in range(N):
    for j in range(i+1, N):
        d = sum(abs(relative_to_zero[i][0] - relative_to_zero[j][0]))
        if d > max_dist:
            max_dist = d
print(max_dist)
