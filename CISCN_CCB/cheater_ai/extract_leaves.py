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

# Extract base_weights
bw_offsets = find_all(b'base_weights')
all_leaves = []
for off in bw_offsets:
    p = off + 12
    if data[p:p+4] == b'[$d#':
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

print(f"Number of trees (leaves): {len(all_leaves)}")

# Look for an extremely negative leaf value
for i, (off, leaves) in enumerate(all_leaves):
    min_leaf = min(leaves)
    if min_leaf < -10:
        print(f"Tree {i} at {off} has a very negative leaf: {min_leaf}")
        # print(leaves)
