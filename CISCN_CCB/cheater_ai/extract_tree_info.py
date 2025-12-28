import struct
import numpy as np

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
for off in sc_offsets:
    # After split_conditions, there should be [$F#L
    # split_conditions is 16 bytes.
    # Check if next bytes are [$F#L
    p = off + 16
    if data[p:p+4] == b'[$F#':
        p += 4
        if data[p:p+1] == b'L':
            p += 1
            count = struct.unpack('>Q', data[p:p+8])[0]
            p += 8
            floats = []
            for _ in range(count):
                val = struct.unpack('>d', data[p:p+8])[0]
                floats.append(val)
                p += 8
            print(f"Found {count} split conditions at {off}")
            # print(floats)
    else:
        # Try different markers
        print(f"split_conditions at {off} has unknown format: {data[p:p+10]}")

# Extract split_indices
si_offsets = find_all(b'split_indices')
for off in si_offsets:
    p = off + 13
    if data[p:p+4] == b'[$i#': # int8
        pass
    elif data[p:p+4] == b'[$I#': # int16
        pass
    elif data[p:p+4] == b'[$l#': # int32
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
            print(f"Found {count} split indices at {off}")
            # print(indices)
