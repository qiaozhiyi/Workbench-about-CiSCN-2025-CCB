import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

sc_offsets = []
pos = data.find(b'split_conditions')
while pos != -1:
    sc_offsets.append(pos)
    pos = data.find(b'split_conditions', pos + 1)

unique_conds = {}
for off in sc_offsets:
    p = off + 16
    if data[p:p+4] == b'[$d#':
        p += 4
        if data[p:p+1] == b'L':
            p += 1
            count = struct.unpack('>Q', data[p:p+8])[0]
            p += 8
            for _ in range(count):
                val = struct.unpack('>f', data[p:p+4])[0]
                unique_conds[val] = unique_conds.get(val, 0) + 1
                p += 4

# Sort by number of occurrences
sorted_conds = sorted(unique_conds.items(), key=lambda x: x[1], reverse=True)
for val, count in sorted_conds:
    if count == 1: # Unique conditions are suspicious
        print(f"Unique condition: {val}")
    elif count > 50:
        # print(f"Common condition: {val} (count {count})")
        pass
