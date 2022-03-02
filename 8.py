lines = open('input_8.txt').read().splitlines()

res = 0

for line in lines:
    # In the first part we only care about the four digit output
    out = line.split('|')[1].split(' ')[1:]
    # 1, 4, 7 and 8 are easy to find, because they are encoded by 2/4/3/7 letters
    for word in out:
        if len(word) in [2, 3, 4, 7]:
            res += 1

print(res)

###
# Second part
###
    
res = 0
for line in lines:
    # Load how 0, 1, ... 9 are encoded - sort letters in each encoding alphabetically
    encodings = line.split('|')[0].split(' ')[:-1]
    encodings = [''.join(sorted(i)) for i in encodings]

    # Count how many times each letter repeats in the encodings
    dic = {x: 0 for x in ['a', 'b', 'c', 'd', 'e', 'f', 'g']}
    for i in encodings:
        for lett in i:
            dic[lett] += 1

    # We use convention where lowercase letters represent the segments as given (mixed
    # up), uppercase the segments as they are supposed to be (i.e. seven corresponds to
    # ACF)

    # Dictionary of mappings from the mixed up segments to the unmixed ones
    mappings = {}

    # find which segments correspond to B, E, F based on how many times a,b,... appear in
    # the encoding
    for key in dic:
        if dic[key] == 4:
            mappings[key] = 'E'
        if dic[key] == 6:
            mappings[key] = 'B'
        if dic[key] == 9:
            mappings[key] = 'F'
            
    # find which two (mixed-up) segments together make up digit one
    for i in range(10):
        if len(encodings[i]) == 2:
            one = encodings[i]

    # find which segments correspond to C, A: both appear eight times in the encodings but
    # segment C is included in the digit one
    for key in dic:
        if dic[key] == 8 and (key in one):
           mappings[key] = 'C' 
        if dic[key] == 8 and not (key in one):
           mappings[key] = 'A' 

    # find which mixed-up segments together make up digit four
    for i in range(10):
        if len(encodings[i]) == 4:
            four = encodings[i]

    # find which segments correspond to D, G: both appear seven times in the encodings but
    # segment D is included in the digit four
    for key in dic:
        if dic[key] == 7 and (key in four):
           mappings[key] = 'D' 
        if dic[key] == 7 and not (key in four):
           mappings[key] = 'G' 

    # The four-digit output value
    out = line.split('|')[1]

    # Translate it from the mixed-up segments to the unmixed ones
    for key in mappings:
        out = out.replace(key, mappings[key])

    # Sort
    out = out.split(' ')[1:]
    out = [''.join(sorted(i)) for i in out]

    # Go to the base 10 representation
    final_map = {'ABCEFG': 0, 'CF': 1, 'ACDEG': 2, 'ACDFG': 3, 'BCDF': 4, 'ABDFG': 5,
        'ABDEFG': 6, 'ACF': 7, 'ABCDEFG': 8, 'ABCDFG': 9}

    out = [final_map[x] for x in out]
    out = 1000*out[0] + 100*out[1] + 10*out[2] + out[3]

    # Keep track of the sum of the results
    res += out

print(res)
