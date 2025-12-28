import struct

def parse_val(data, offset):
    char = data[offset:offset+1]
    offset += 1
    if char == b'{':
        d = {}
        while data[offset:offset+1] != b'}':
            # Key is a string (no S marker)
            length, offset = parse_val(data, offset)
            key = data[offset:offset+length].decode('utf-8', errors='ignore')
            offset += length
            # Value
            val, offset = parse_val(data, offset)
            d[key] = val
        return d, offset + 1
    elif char == b'[':
        l = []
        if data[offset:offset+1] == b'#':
            offset += 1
            num, offset = parse_val(data, offset)
            for _ in range(num):
                val, offset = parse_val(data, offset)
                l.append(val)
        else:
            while data[offset:offset+1] != b']':
                val, offset = parse_val(data, offset)
                l.append(val)
        return l, offset + 1
    elif char == b'L':
        val = struct.unpack('>q', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'l':
        val = struct.unpack('>i', data[offset:offset+4])[0]
        return val, offset + 4
    elif char == b'I':
        val = struct.unpack('>h', data[offset:offset+2])[0]
        return val, offset + 2
    elif char == b'i':
        val = struct.unpack('>b', data[offset:offset+1])[0]
        return val, offset + 1
    elif char == b'U':
        val = struct.unpack('>B', data[offset:offset+1])[0]
        return val, offset + 1
    elif char == b'F':
        val = struct.unpack('>d', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'd':
        val = struct.unpack('>f', data[offset:offset+4])[0]
        return val, offset + 4
    elif char == b'S':
        length, offset = parse_val(data, offset)
        val = data[offset:offset+length].decode('utf-8', errors='ignore')
        return val, offset + length
    elif char == b'B':
        return data[offset] != 0, offset + 1
    elif char == b'Z':
        return None, offset
    elif char == b'T':
        return True, offset
    elif char == b'F': # Wait, F is float64 in my other check, but T/F is bool.
        # UBJSON uses T and F.
        return False, offset
    else:
        raise ValueError(f"Unknown char {char} at {offset-1}")

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

model, _ = parse_val(data, 0)
if 'learner' in model and 'attributes' in model['learner']:
    print("Attributes:", model['learner']['attributes'])
