lines = open('input_14.txt').readlines()
lines = [l.replace('\n', '') for l in lines]

# Load pair insertion rules as a dictionary
d = {}

for line in lines[2:]:
    f, s = line.split(' -> ')
    d[f] = s

# Polymer template
text = lines[0]

# Perform ten polymerization steps - we can do it directly
for i in range(10):
    new_text = ''
    for j in range(len(text)-1):
        new_text += text[j]
        new_text += d[text[j:j+2]]
    new_text += text[-1]
    text = new_text

# Count symbols in the result
counts_el = {}
for t in text:
    if t in counts_el:
        counts_el[t] += 1
    else:
        counts_el[t] = 1

# Find most and least common element
mi = 1e12
ma = 0
for k in counts_el:
    if counts_el[k] > ma:
        ma = counts_el[k]
    elif counts_el[k] < mi:
        mi = counts_el[k]

print(ma - mi)

####
# second problem
####

# To speed things up, we will keep track of the number of pairs as a dictionary, indexed
# by the two-character string

# Initialize the dictionary from the pair insertion rules
counts = {}
for k in d:
    counts[k] = 0

# Count pairs in the polymer template
text = lines[0]
for j in range(len(text)-1):
    counts[text[j:j+2]] += 1

# Perform 40 iterations
for i in range(40):
    
    # Updated state
    new_counts = {}
    for k in d:
        new_counts[k] = 0

    # Polymerization rules - for each type of pair
    for k in counts:

        # Original pair (e.g. PH)
        p1, p3 = k[0], k[1]

        # New middle character (e.g. V)
        p2 = d[k]

        # We have contributions to both PV and VH
        new_counts[p1 + p2] += counts[k]
        new_counts[p2 + p3] += counts[k]

    counts = new_counts

# The dictionary "counts" keeps information about how many times any given pairing appears
# in the result. We convert this into how many times each element appears in the result.
counts_el = {}
for pair in counts:
    for element in pair:
        if element in counts_el:
            counts_el[element] += counts[pair]
        else: 
            counts_el[element] = counts[pair]

# Notice that each element - with the exception of the first and last one in the initial
# polymer template - is double counted and we have to correct for this. For example
# in ....PHV..., H would be counted in both PH and HV.
for k in counts_el:
    if k in [text[0], text[-1]]: # First and last in the initial template
        counts_el[k] = (counts_el[k]+1)//2
    else:
        counts_el[k] = counts_el[k]//2

# Find most and least common element
mi = 1e12
ma = 0
for k in counts_el:
    if counts_el[k] > ma:
        ma = counts_el[k]
    elif counts_el[k] < mi:
        mi = counts_el[k]

print(ma - mi)
