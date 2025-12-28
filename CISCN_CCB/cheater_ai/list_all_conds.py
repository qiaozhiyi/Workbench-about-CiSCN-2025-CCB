import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

sc_offsets = []
pos = data.find(b'split_conditions')
while pos != -1:
    sc_offsets.append(pos)
    pos = data.find(b'split_conditions', pos + 1)

all_conds = set()
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
                all_conds.add(val)
                p += 4

for c in sorted(list(all_conds)):
    print(c)
