import struct
import json

def parse_val(data, offset):
    char = data[offset:offset+1]
    if char == b'{':
        offset += 1
        d = {}
        while data[offset:offset+1] != b'}':
            # Key is always a string preceded by L?
            if data[offset:offset+1] != b'L':
                # Maybe it's not always L. Let's see.
                key, offset = parse_val(data, offset)
            else:
                offset += 1
                length = struct.unpack('>Q', data[offset:offset+8])[0]
                offset += 8
                key = data[offset:offset+length].decode('utf-8')
                offset += length
            
            val, offset = parse_val(data, offset)
            d[key] = val
        return d, offset + 1
    elif char == b'[':
        offset += 1
        l = []
        if data[offset:offset+1] == b'#':
            offset += 1
            # Number of elements
            num_elements, offset = parse_val(data, offset)
            for _ in range(num_elements):
                val, offset = parse_val(data, offset)
                l.append(val)
        else:
            while data[offset:offset+1] != b']':
                val, offset = parse_val(data, offset)
                l.append(val)
        return l, offset + 1
    elif char == b'L':
        offset += 1
        val = struct.unpack('>Q', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'I':
        offset += 1
        val = struct.unpack('>q', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'F':
        offset += 1
        val = struct.unpack('>d', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'S':
        offset += 1
        # String is S followed by length-prefixed data (L)
        if data[offset:offset+1] == b'L':
            offset += 1
            length = struct.unpack('>Q', data[offset:offset+8])[0]
            offset += 8
            val = data[offset:offset+length].decode('utf-8')
            return val, offset + length
        else:
            raise ValueError(f"S not followed by L at {offset}")
    elif char == b'B':
        offset += 1
        val = data[offset] != 0
        return val, offset + 1
    elif char == b'N': # Null?
        return None, offset + 1
    else:
        # Debug
        print(f"Unknown char {char} at {offset}")
        print(f"Context: {data[max(0, offset-20):offset+20]}")
        raise ValueError(f"Unknown char {char}")

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

model, _ = parse_val(data, 0)
with open('model.json', 'w') as f:
    json.dump(model, f, indent=2)
print("Model parsed successfully.")
