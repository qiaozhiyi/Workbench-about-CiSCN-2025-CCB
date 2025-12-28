import struct

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

pos = data.find(b'split_conditions')
p = pos + 16 + 4 + 1 + 8
count = 11
conds = [struct.unpack('>f', data[p+i*4:p+i*4+4])[0] for i in range(count)]

pos_idx = data.find(b'split_indices')
p_idx = pos_idx + 13 + 4 + 1 + 8
indices = [struct.unpack('>i', data[p_idx+i*4:p_idx+i*4+4])[0] for i in range(count)]

for i in range(count):
    print(f"Node {i}: index {indices[i]}, condition {conds[i]}")
