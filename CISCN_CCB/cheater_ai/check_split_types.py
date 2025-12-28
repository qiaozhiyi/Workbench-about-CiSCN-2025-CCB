import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

def find_all(pattern):
    offsets = []
    pos = data.find(pattern)
    while pos != -1:
        offsets.append(pos)
        pos = data.find(pattern, pos + 1)
    return offsets

st_pos = find_all(b'split_type')
for i, pos in enumerate(st_pos):
    p = pos + 10 + 4 + 1 + 8
    count_pos = pos + 10 + 4 + 1
    count = struct.unpack('>Q', data[count_pos:count_pos+8])[0]
    types = [data[p+j] for j in range(count)]
    if 1 in types:
        print(f"Tree {i} has categorical splits!")
