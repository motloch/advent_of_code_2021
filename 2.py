lines = open('input_2.txt').read().splitlines()

# First part
horizontal = 0
depth = 0

for line in lines:
    t, n = line.split(' ')
    if t == 'forward':
        horizontal += int(n)
    if t == 'up':
        depth -= int(n)
    if t == 'down':
        depth += int(n)
        
print(horizontal*depth)
    
# Second part
horizontal = 0
depth = 0
aim = 0

for line in lines:
    t, n = line.split(' ')
    if t == 'forward':
        horizontal += int(n)
        depth += aim*int(n)
    if t == 'up':
        aim -= int(n)
    if t == 'down':
        aim += int(n)
        
print(horizontal*depth)
