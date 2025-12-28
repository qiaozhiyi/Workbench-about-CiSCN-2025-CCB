import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

def inspect_tree(tree_idx):
    si_pos = find_all(b'split_indices')[tree_idx]
    count_pos = si_pos + 13 + 4 + 1
    count = struct.unpack('>Q', data[count_pos:count_pos+8])[0]
    p_si = si_pos + 13 + 4 + 1 + 8
    indices = [struct.unpack('>i', data[p_si+j*4:p_si+j*4+4])[0] for j in range(count)]
    
    sc_pos = find_all(b'split_conditions')[tree_idx]
    p_sc = sc_pos + 16 + 4 + 1 + 8
    conds = [struct.unpack('>f', data[p_sc+j*4:p_sc+j*4+4])[0] for j in range(count)]
    
    bw_pos = find_all(b'base_weights')[tree_idx]
    p_bw = bw_pos + 12 + 4 + 1 + 8
    weights = [struct.unpack('>f', data[p_bw+j*4:p_bw+j*4+4])[0] for j in range(count)]
    
    lc_pos = find_all(b'left_children')[tree_idx]
    p_lc = lc_pos + 13 + 4 + 1 + 8
    lefts = [struct.unpack('>i', data[p_lc+j*4:p_lc+j*4+4])[0] for j in range(count)]
    
    rc_pos = find_all(b'right_children')[tree_idx]
    p_rc = rc_pos + 14 + 4 + 1 + 8
    rights = [struct.unpack('>i', data[p_rc+j*4:p_rc+j*4+4])[0] for j in range(count)]
    
    print(f"--- Tree {tree_idx} ---")
    for i in range(count):
        print(f"Node {i}: index {indices[i]}, cond {conds[i]}, weight {weights[i]}, L {lefts[i]}, R {rights[i]}")

def find_all(pattern):
    offsets = []
    pos = data.find(pattern)
    while pos != -1:
        offsets.append(pos)
        pos = data.find(pattern, pos + 1)
    return offsets

inspect_tree(37)
inspect_tree(41)
