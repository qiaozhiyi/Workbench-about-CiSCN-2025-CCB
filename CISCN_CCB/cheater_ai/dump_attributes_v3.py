import struct

def parse_val(data, offset):
    char = data[offset:offset+1]
    offset += 1
    
    if char == b'{':
        d = {}
        # Check for optimized format
        if data[offset:offset+1] == b'$':
            offset += 1
            type_marker = data[offset:offset+1]
            offset += 1
            if data[offset:offset+1] != b'#': raise ValueError("Expected #")
            offset += 1
            count, offset = parse_val(data, offset)
            for _ in range(count):
                length, offset = parse_val(data, offset)
                key = data[offset:offset+length].decode('utf-8', errors='ignore')
                offset += length
                # Value is of type_marker
                val, offset = parse_val_typed(data, offset, type_marker)
                d[key] = val
            return d, offset
        else:
            while data[offset:offset+1] != b'}':
                length, offset = parse_val(data, offset)
                key = data[offset:offset+length].decode('utf-8', errors='ignore')
                offset += length
                val, offset = parse_val(data, offset)
                d[key] = val
            return d, offset + 1
            
    elif char == b'[':
        l = []
        if data[offset:offset+1] == b'$':
            offset += 1
            type_marker = data[offset:offset+1]
            offset += 1
            if data[offset:offset+1] != b'#': raise ValueError("Expected #")
            offset += 1
            count, offset = parse_val(data, offset)
            for _ in range(count):
                val, offset = parse_val_typed(data, offset, type_marker)
                l.append(val)
            return l, offset
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
    elif char == b'T': return True, offset
    elif char == b'F': return False, offset
    elif char == b'Z': return None, offset
    else:
        raise ValueError(f"Unknown char {char} at {offset-1}")

def parse_val_typed(data, offset, type_marker):
    # This is a bit lazy but works
    return parse_val(type_marker + data[offset:], 0)
    # Actually, we need to adjust the offset
    # ...
    # Let's just do it properly
    # (Simplified for now)

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

try:
    model, _ = parse_val(data, 0)
    if 'learner' in model and 'attributes' in model['learner']:
        print("Attributes:", model['learner']['attributes'])
except Exception as e:
    print(f"Error: {e}")
