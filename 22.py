import numpy as np

# Load input file
lines = open('input_22.txt').read().splitlines()

# Maximal absolute value of x/y/z during initialization
N = 50

# Because of small size, we can keep track of on/off cubes directly.
# Starting with all cubes off.
arr = np.zeros((2*N+1, 2*N+1, 2*N+1), dtype = bool)

# Go through the instructions and turn cubes on / off
for line in lines:
    # Get command as 'on' or 'off' and the coordinates in xmin, xmax, ymin, ...
    command, coord = line.split(' ')  
    xc, yc, zc = coord.split(',')
    xmin,xmax = map(int, xc[2:].split('..'))
    ymin,ymax = map(int, yc[2:].split('..'))
    zmin,zmax = map(int, zc[2:].split('..'))

    # Restrict to the initialization region
    xmin = max(-N,xmin)
    ymin = max(-N,ymin)
    zmin = max(-N,zmin)
    xmax = min(N,xmax)
    ymax = min(N,ymax)
    zmax = min(N,zmax)

    # Trun cubes on/off
    if command == 'on':
        arr[xmin+N:xmax+N+1, ymin+N:ymax+N+1, zmin+N:zmax+N+1] = True
    else:
        arr[xmin+N:xmax+N+1, ymin+N:ymax+N+1, zmin+N:zmax+N+1] = False

# Count how many cubes are turned on
print(np.sum(arr))

####
# Second problem
####

class Cuboid:
    """
    Abstract class that represents a cuboid, effectively packing the extent of the x/y/z
    coordinates into a single object.
    """
    def __init__(self, x1, x2, y1, y2, z1, z2):
        """
        coordinates of the cuboid edges (x1, x2 are included)
        """
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
        self.z1 = min(z1, z2)
        self.z2 = max(z1, z2)

def intersect_1d_intervals(c1x1, c1x2, c2x1, c2x2):
    """
    Given two overlapping intervals [c1x1, c1x2] and [c2x1, c2x2], split [c1x1, c1x2] into
    (up to three) smaller intervals that either fully intersect with [c2x1, c2x2], or have
    no common point with this second interval.
    
    Returns a list of tuples representing the smaller intervals. The first element of each
    tuple is a list with two elements representing the boundaries of the interval, the
    second element is a boolean representing if the smaller interval overlaps with c2
    or has no intersect.

    Notice that union of the smaller intervals represented by the first elements of each
    output tuple give together the first interval.
    """

    # second interval fully in the first
    if c1x1 < c2x1 <= c2x2 < c1x2:
        lims = [
                    ([c1x1, c2x1-1], False), 
                    ([c2x1, c2x2], True), 
                    ([c2x2+1, c1x2], False)
                ]
    # partial overlaps
    elif c2x1 <= c1x1 <= c2x2 < c1x2:
        lims = [
                    ([c1x1, c2x2], True), 
                    ([c2x2+1, c1x2], False)
                ]
    elif c1x1 < c2x1 <= c1x2 <= c2x2:
        lims = [
                    ([c1x1, c2x1-1], False), 
                    ([c2x1, c1x2], True)
                ]
    # first interval fully in the second
    elif c2x1 <= c1x1 <= c1x2 <= c2x2:
        lims = [
                    ([c1x1, c1x2], True), 
                ]
    return lims

def subtract_from_cuboid(c1, c2):
    """
    Given two cuboids, return an array of cuboids making up the "cubes from c1 that are not in c2"

    The idea is to split the c1 cuboid into a union of smaller cuboids and keep them all,
    except for the one that is fully in c2
    """

    # If there is no intersection between the two cuboids, we do not subtract anything
    x_isect = (c1.x1 <= c2.x1 <= c1.x2) or (c2.x1 <= c1.x1 <= c2.x2)
    y_isect = (c1.y1 <= c2.y1 <= c1.y2) or (c2.y1 <= c1.y1 <= c2.y2)
    z_isect = (c1.z1 <= c2.z1 <= c1.z2) or (c2.z1 <= c1.z1 <= c2.z2)
    if (not x_isect) or (not y_isect) or (not z_isect):
        return [c1]

    # Otherwise in each direction look at the range of coordinates that are present only
    # in the first cuboid / overlap with the second cuboid
    x_ints = intersect_1d_intervals(c1.x1, c1.x2, c2.x1, c2.x2)
    y_ints = intersect_1d_intervals(c1.y1, c1.y2, c2.y1, c2.y2)
    z_ints = intersect_1d_intervals(c1.z1, c1.z2, c2.z1, c2.z2)

    # Now cuboid one is a "sum" of all possible "products" of subintervals from x_lims,
    # y_lims and z_lims

    # The volume representing "cubes from c1 that are not in c2" can be obtained if we
    # throw away the one cuboid that is fully within cuboid two. We can tell it apart,
    # because it intersects with c1 in all dimensions
    
    cuboids_only_in_c1 = []
    for x_int, x_overlaps_with_c2 in x_ints:
        for y_int, y_overlaps_with_c2 in y_ints:
            for z_int, z_overlaps_with_c2 in z_ints:
                #Is this cuboid fully part of the second input cuboid?
                if x_overlaps_with_c2 and y_overlaps_with_c2 and z_overlaps_with_c2:
                    continue 
                else:
                    cuboids_only_in_c1.append(Cuboid(
                                x_int[0], x_int[1],
                                y_int[0], y_int[1],
                                z_int[0], z_int[1]
                                ))
    return cuboids_only_in_c1

# Keep track of the cuboids in which the cubes are "on"
cuboids = []

# Go through the instructions and turn cubes on / off
for line in lines:
    # Get command as 'on' or 'off' and the coordinates in xmin, xmax, ymin, ...
    command, coord = line.split(' ')  
    xc, yc, zc = coord.split(',')
    xmin,xmax = map(int, xc[2:].split('..'))
    ymin,ymax = map(int, yc[2:].split('..'))
    zmin,zmax = map(int, zc[2:].split('..'))

    instruction_cuboid = Cuboid(xmin, xmax, ymin, ymax, zmin, zmax)

    # Keep track of all the cuboids with cubes that are on
    if command == 'on':
        new_cuboids = [instruction_cuboid]
    else:
        new_cuboids = []

    # Add all of the old cuboids with the currently processed cuboid subtracted
    # (if the instruction is "on", we have already included currently processed cuboid in
    # the new_cuboids array and we should not double count it)
    for cuboid in cuboids:
        # In general, subtraction gives several cuboids
        residual  = subtract_from_cuboid(cuboid, instruction_cuboid)
        for r in residual:
            new_cuboids.append(r)

    cuboids = new_cuboids

# Total volume that is turned on
vol = 0
for cuboid in cuboids:
    vol += (cuboid.x2 - cuboid.x1 + 1)*(cuboid.y2 - cuboid.y1 + 1)*(cuboid.z2 - cuboid.z1 + 1)
print(vol)
