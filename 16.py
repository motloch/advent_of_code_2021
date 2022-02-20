from math import prod

def hex_to_binary(txt):
    """
    Convert hexadecimal string to binary string
    """
    return "{0:08b}".format(int(txt, 16)) 

# Load input
line = open('input_16.txt').readlines()[0].replace('\n', '')
line = hex_to_binary(line)

class packet():
    """
    Class representing a packet: 
        integer representing T, 
        integer representing V, 
        integer representing literal value (if ID 4)
        array representing subpackets
    """
    def __init__(self):
        self.v = 0
        self.t = 0
        self.val = 0
        self.ops = []

def read_value(txt):
    """
    Reads the literal value from the string of zeros and ones

    Returns the value as an integer and a position at which the next packet starts
    """
    res = ''     # result as a binary string
    pos = 0      # where we currently are in the string
    cont = True  # whether to continue reading
    while cont:
        bits = txt[pos:pos+5] #everything is in groups of five bits
        if bits[0] == '0':    #check whether this group is the final one
            cont = False
        res += bits[1:]
        pos += 5
    return int(res, 2), pos

def load_packet(txt):
    """
    Return packet build from a string of zeros and ones, return
    the number of bits used in construction of this packet
    """
    op = packet()           # packet we will return
    op.v = int(txt[:3], 2)  # first three bits are V
    op.t = int(txt[3:6], 2) # next three bits are T

    # If T is 4, we have a literal value operator
    if op.t == 4:
        op.val, start = read_value(txt[6:])
        return op, 6 + start
    else:
        length_type_id = txt[6]
        if length_type_id == '0':
            # In this case, the next 15 bits represent the string length of the subpackets
            total_length = int(txt[7:22], 2)

            start = 22 # Where the next subpacket starts

            # Load the subpackets
            while start < 22 + total_length:
                opB, length = load_packet(txt[start:])
                op.ops.append(opB)
                start += length
            return op, start
        else:
            # In this case, the next 11 bits represent the number of subpackets
            num_subpackets = int(txt[7:18], 2)
            start = 18
            for i in range(num_subpackets):
                opB, length = load_packet(txt[start:])
                op.ops.append(opB)
                start += length
            return op, start

#op, _ = load_packet('110100101111111000101000')
#op, _ = load_packet('00111000000000000110111101000101001010010001001000000000')
#op, _ = load_packet('11101110000000001101010000001100100000100011000001100000')

def count_version_sum(op):
    """
    Given a packet, count the sum of the version numbers of the opearator and all sub
    """
    result = op.v
    for opB in op.ops:
        result += count_version_sum(opB)
    return result

#print(count_version_sum(load_packet(hex_to_binary('8A004A801A8002F478'))[0]))
#print(count_version_sum(load_packet(hex_to_binary('620080001611562C8802118E34'))[0]))
#print(count_version_sum(load_packet(hex_to_binary('C0015000016115A2E0802F182340'))[0]))
#print(count_version_sum(load_packet(hex_to_binary('A0016C880162017C3686B18A3D4780'))[0]))
print(count_version_sum(load_packet(line)[0]))

def evaluate(op):
    """
    Evaluate the operator
    """
    if op.t == 4:
        return op.val
    elif op.t == 0:
        return sum([evaluate(opB) for opB in op.ops])
    elif op.t == 1:
        return prod([evaluate(opB) for opB in op.ops])
    elif op.t == 2:
        return min([evaluate(opB) for opB in op.ops])
    elif op.t == 3:
        return max([evaluate(opB) for opB in op.ops])
    elif op.t == 5:
        return int(evaluate(op.ops[0]) > evaluate(op.ops[1]))
    elif op.t == 6:
        return int(evaluate(op.ops[0]) < evaluate(op.ops[1]))
    elif op.t == 7:
        return int(evaluate(op.ops[0]) == evaluate(op.ops[1]))
    else:
        print('crash')
        exit()

print(evaluate(load_packet(line)[0]))
