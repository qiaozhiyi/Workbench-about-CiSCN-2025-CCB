import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

bw_offsets = []
pos = data.find(b'base_weights')
while pos != -1:
    bw_offsets.append(pos)
    pos = data.find(b'base_weights', pos + 1)

for off in bw_offsets:
    p = off + 12
    if data[p:p+4] == b'[$d#':
        p += 4
        if data[p:p+1] == b'L':
            p += 1
            count = struct.unpack('>Q', data[p:p+8])[0]
            p += 8
            for _ in range(count):
                val = struct.unpack('>f', data[p:p+4])[0]
                if abs(val) > 5:
                    print(f"Large weight: {val} at offset {p-4}")
                p += 4
