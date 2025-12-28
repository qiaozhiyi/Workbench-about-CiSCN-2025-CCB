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

si_pos = find_all(b'split_indices')
max_nodes = 0
max_tree = -1
for i, pos in enumerate(si_pos):
    count_pos = pos + 13 + 4 + 1
    count = struct.unpack('>Q', data[count_pos:count_pos+8])[0]
    if count > max_nodes:
        max_nodes = count
        max_tree = i

print(f"Max nodes: {max_nodes} in Tree {max_tree}")
