import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

sc_offsets = []
pos = data.find(b'split_conditions')
while pos != -1:
    sc_offsets.append(pos)
    pos = data.find(b'split_conditions', pos + 1)

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
                if abs(val - round(val)) < 1e-7 and val != 0:
                    print(f"Integer-like condition: {val} at offset {p-4}")
                p += 4
