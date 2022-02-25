from math import floor

#target area
xmin = 201
xmax = 230
ymin = -99
ymax = -65

#range of x velocities to try
vxmax = xmax
vxmin = 1

#highest y position over all trajectories
global_max_y = 0
#number of distinct initial velocities that end up in the target
ends_in_target = 0

#try a range of initial velocities (x and y components)
for vx0 in range(0, vxmax+1):
    for vy0 in range(-vxmax, vxmax):
        # initialize the throw parameters
        vx = vx0
        vy = vy0
        x = 0
        y = 0
        # maximal y coordinate of the current throw 
        current_y_max = 0
        # is the throw passing through the target area?
        current_counted = False

        # model the throw step by step until we have no chance of reaching the target area
        while (y >= ymin) and (x <= xmax):
            
            # update position
            x += vx
            y += vy
            if y > current_y_max:
                current_y_max = y

            # decrease of x velocity due to drag
            vx -= 1
            if vx < 0:
                vx = 0

            # decrease of y velocity due to gravity
            vy -= 1

            # if we hit target area
            if (xmin <= x) and (x <= xmax) and (ymin <= y) and (y <= ymax):
                if current_y_max > global_max_y:
                    global_max_y = current_y_max
                if not current_counted:
                    ends_in_target += 1
                    current_counted = True

print(global_max_y)
print(ends_in_target)
