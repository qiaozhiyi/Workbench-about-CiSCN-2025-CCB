import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

def get_tree_info(tree_idx):
    si_pos = find_all(b'split_indices')[tree_idx]
    count = struct.unpack('>Q', data[si_pos+13+4+1:si_pos+13+4+1+8])[0]
    p_si = si_pos + 13+4+1+8
    indices = [struct.unpack('>i', data[p_si+j*4:p_si+j*4+4])[0] for j in range(count)]
    sc_pos = find_all(b'split_conditions')[tree_idx]
    p_sc = sc_pos + 16+4+1+8
    conds = [struct.unpack('>f', data[p_sc+j*4:p_sc+j*4+4])[0] for j in range(count)]
    return indices, conds

def find_all(pattern):
    offsets = []
    pos = data.find(pattern)
    while pos != -1:
        offsets.append(pos)
        pos = data.find(pattern, pos + 1)
    return offsets

for t in [4, 6, 9, 16, 26, 38, 42]:
    indices, conds = get_tree_info(t)
    for i, idx in enumerate(indices):
        if idx == 5:
            print(f"Tree {t} uses feature 5 with threshold {conds[i]}")

for t in [37, 41]:
    indices, conds = get_tree_info(t)
    for i, idx in enumerate(indices):
        if idx == 3:
            print(f"Tree {t} uses feature 3 with threshold {conds[i]}")
