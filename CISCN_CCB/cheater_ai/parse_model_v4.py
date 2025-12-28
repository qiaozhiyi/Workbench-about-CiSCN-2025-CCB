import struct
import json

def parse_ubjson(data, offset):
    char = data[offset:offset+1]
    offset += 1
    
    if char == b'{':
        # Object
        res = {}
        # Check for optimized format
        if data[offset:offset+1] == b'$':
            offset += 1
            val_type = data[offset:offset+1]
            offset += 1
            if data[offset:offset+1] != b'#':
                raise ValueError("Expected # after $ in object")
            offset += 1
            count, offset = parse_ubjson(data, offset)
            for _ in range(count):
                key, offset = parse_ubjson(data, offset)
                # Value is of val_type
                # We need to call a specific parser for val_type
                val, offset = parse_ubjson_typed(data, offset, val_type)
                res[key] = val
        else:
            while data[offset:offset+1] != b'}':
                key, offset = parse_ubjson(data, offset)
                val, offset = parse_ubjson(data, offset)
                res[key] = val
            offset += 1
        return res, offset
    
    elif char == b'[':
        # Array
        res = []
        if data[offset:offset+1] == b'$':
            offset += 1
            val_type = data[offset:offset+1]
            offset += 1
            if data[offset:offset+1] != b'#':
                raise ValueError("Expected # after $ in array")
            offset += 1
            count, offset = parse_ubjson(data, offset)
            for _ in range(count):
                val, offset = parse_ubjson_typed(data, offset, val_type)
                res.append(val)
        else:
            while data[offset:offset+1] != b']':
                val, offset = parse_ubjson(data, offset)
                res.append(val)
            offset += 1
        return res, offset
    
    elif char == b'S':
        # String. Length follows.
        length, offset = parse_ubjson(data, offset)
        val = data[offset:offset+length].decode('utf-8')
        return val, offset + length
    
    elif char == b'L':
        # Int64
        val = struct.unpack('>q', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'l':
        # Int32
        val = struct.unpack('>i', data[offset:offset+4])[0]
        return val, offset + 4
    elif char == b'I':
        # Int16
        val = struct.unpack('>h', data[offset:offset+2])[0]
        return val, offset + 2
    elif char == b'i':
        # Int8
        val = struct.unpack('>b', data[offset:offset+1])[0]
        return val, offset + 1
    elif char == b'U':
        # Uint8
        val = struct.unpack('>B', data[offset:offset+1])[0]
        return val, offset + 1
    elif char == b'F':
        # Float64 (In some UBJSON it's 'D', but here it seems to be 'F')
        val = struct.unpack('>d', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'd':
        # Float32
        val = struct.unpack('>f', data[offset:offset+4])[0]
        return val, offset + 4
    elif char == b'T':
        return True, offset
    elif char == b'F': # Wait, 'F' is both float and False? 
        # Actually UBJSON uses 'F' for False and 'D' for float.
        # But my strings showed 'F' for float values.
        # Let's check the context.
        pass
    elif char == b'Z':
        return None, offset
    
    # In some contexts, the length-prefixed data is just 'L' + length + data
    # (without the 'S' marker if it's a key).
    # But wait, UBJSON says keys are strings without the 'S' marker.
    # So if we are in an object and expect a key, we just read a string.
    # But strings start with a length? No, strings in UBJSON start with 'S'.
    # Wait, if there's no 'S', maybe it's the raw length?
    
    # Let's handle the case where 'L' is the first byte but it's used as a string.
    # Actually, let's just use the 'S' logic if we see it.
    
    raise ValueError(f"Unknown marker {char} at {offset-1}")

def parse_ubjson_typed(data, offset, val_type):
    # This is like parse_ubjson but the marker is already known.
    # We need to call the right struct.unpack.
    if val_type == b'L':
        val = struct.unpack('>q', data[offset:offset+8])[0]
        return val, offset + 8
    elif val_type == b'l':
        val = struct.unpack('>i', data[offset:offset+4])[0]
        return val, offset + 4
    elif val_type == b'F':
        val = struct.unpack('>d', data[offset:offset+8])[0]
        return val, offset + 8
    # ... add others as needed
    else:
        # Fallback
        # We might need to prepend the val_type and call parse_ubjson
        return parse_ubjson(val_type + data[offset:], 0) # This is inefficient

# Wait, the simplest way is to fix the previous parser.
# The previous parser failed because 'daily_trans_count' was not preceded by 'S'.
# This means keys in objects are NOT preceded by 'S'.
# They are just Length-prefixed strings.
# And UBJSON says keys are always strings and they DON'T have the 'S' marker.
# They just start with the length (which is an integer type marker).

# Let's try one more time.
