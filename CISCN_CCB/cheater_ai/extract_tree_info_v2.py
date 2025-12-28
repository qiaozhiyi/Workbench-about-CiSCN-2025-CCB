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

# Extract split_conditions
sc_offsets = find_all(b'split_conditions')
all_conditions = []
for off in sc_offsets:
    p = off + 16
    if data[p:p+4] == b'[$d#':
        p += 4
        if data[p:p+1] == b'L':
            p += 1
            count = struct.unpack('>Q', data[p:p+8])[0]
            p += 8
            floats = []
            for _ in range(count):
                val = struct.unpack('>f', data[p:p+4])[0]
                floats.append(val)
                p += 4
            all_conditions.append((off, floats))

# Extract split_indices
si_offsets = find_all(b'split_indices')
all_indices = []
for off in si_offsets:
    p = off + 13
    if data[p:p+4] == b'[$l#':
        p += 4
        if data[p:p+1] == b'L':
            p += 1
            count = struct.unpack('>Q', data[p:p+8])[0]
            p += 8
            indices = []
            for _ in range(count):
                val = struct.unpack('>i', data[p:p+4])[0]
                indices.append(val)
                p += 4
            all_indices.append((off, indices))

# Extract leaf_values
lv_offsets = find_all(b'leaf_values')
all_leaves = []
for off in lv_offsets:
    p = off + 11
    if data[p:p+4] == b'[$f#': # float32
        p += 4
    elif data[p:p+4] == b'[$d#': # float32 (in some UBJSON d is float32)
        p += 4
    if data[p:p+1] == b'L':
        p += 1
        count = struct.unpack('>Q', data[p:p+8])[0]
        p += 8
        leaves = []
        for _ in range(count):
            val = struct.unpack('>f', data[p:p+4])[0]
            leaves.append(val)
            p += 4
        all_leaves.append((off, leaves))

# Print summary
print(f"Number of trees (conditions): {len(all_conditions)}")
print(f"Number of trees (indices): {len(all_indices)}")
print(f"Number of trees (leaves): {len(all_leaves)}")

# Look for suspicious conditions
# Thresholds that are very specific (many decimals) or unique.
for off, conds in all_conditions:
    for c in conds:
        # Check if the float has many decimals or is an integer-like float
        if abs(c - round(c)) > 1e-6:
             pass # normal
        # Actually, let's just print all unique conditions
        pass

unique_conds = set()
for _, conds in all_conditions:
    for c in conds:
        unique_conds.add(c)

print(f"Number of unique split conditions: {len(unique_conds)}")
# print(sorted(list(unique_conds)))
