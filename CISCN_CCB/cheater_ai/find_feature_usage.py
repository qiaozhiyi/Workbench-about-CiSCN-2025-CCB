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
for i, pos in enumerate(si_pos):
    p = pos + 13 + 4 + 1 + 8
    # Read count from the model
    count_pos = pos + 13 + 4 + 1
    count = struct.unpack('>Q', data[count_pos:count_pos+8])[0]
    indices = [struct.unpack('>i', data[p+j*4:p+j*4+4])[0] for j in range(count)]
    if 3 in indices:
        print(f"Tree {i} uses feature 3 (merchant_code_hash)")
    if 5 in indices:
        print(f"Tree {i} uses feature 5 (pos_terminal_id)")
