import struct

def parse_custom_format(data, offset=0):
    char = data[offset:offset+1]
    if char == b'{':
        offset += 1
        d = {}
        while data[offset:offset+1] != b'}':
            key, offset = parse_custom_format(data, offset)
            val, offset = parse_custom_format(data, offset)
            d[key] = val
        return d, offset + 1
    elif char == b'[':
        offset += 1
        l = []
        if data[offset:offset+1] == b'#':
            offset += 1
            num_elements, offset = parse_custom_format(data, offset)
            for _ in range(num_elements):
                val, offset = parse_custom_format(data, offset)
                l.append(val)
        else:
            while data[offset:offset+1] != b']':
                val, offset = parse_custom_format(data, offset)
                l.append(val)
        return l, offset + 1
    elif char == b'L':
        offset += 1
        val = struct.unpack('>Q', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'S':
        offset += 1
        length, offset = parse_custom_format(data, offset)
        val = data[offset:offset+length].decode('utf-8')
        return val, offset + length
    elif char == b'F':
        offset += 1
        val = struct.unpack('>d', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'I':
        offset += 1
        val = struct.unpack('>q', data[offset:offset+8])[0]
        return val, offset + 8
    elif char == b'B':
        offset += 1
        val = data[offset] != 0
        return val, offset + 1
    else:
        # If it's not a known type, maybe it's a raw string in a key?
        # Let's see if we can handle the 'learner' case.
        # Wait, if 'learner' is not prefixed by S, how is it parsed?
        # Let's look at the bytes again.
        # b'{L\x00\x00\x00\x00\x00\x00\x00\x07learner'
        # Ah! The key is 'learner'. It started with L. 
        # But L is supposed to be a Long.
        # Maybe keys are always S type? No, the S is missing.
        # Wait, maybe L + 8 bytes + string IS a type? 
        # But then what is S?
        # Let's try this: if we see L, and we are in a dictionary key position...
        # No, let's look at the bytes again.
        # b'{L\x00\x00\x00\x00\x00\x00\x00\x07learner'
        # If L is 7, then the next 7 bytes are 'learner'.
        # So L + 8 bytes of length + length bytes of data.
        # But then how does #L work? #L 10 -> 10 elements. 
        # If L always consumed data, then #L 10 would consume 10 bytes of data!
        # So L must be just the number.
        # Then how is 'learner' parsed?
        # Maybe 'learner' is NOT a key, but part of some other structure?
        # No, it's a dict.
        
        print(f"Error at offset {offset}: unknown char {char}")
        print(f"Context: {data[max(0, offset-20):offset+20]}")
        raise ValueError(f"Unknown type marker {char} at offset {offset}")

with open('fraud_detector_supply_chain.pth', 'rb') as f:
    data = f.read()

# Let's try a different approach. Maybe it's a known format like MessagePack or similar?
# No, MessagePack markers are different.
# What if it's a very simple format:
# { -> dict
# [ -> list
# S -> string (S + length_type + data)
# L -> 64-bit int
# F -> 64-bit float
# ...
# Wait, if keys don't have S, maybe keys are just raw strings?
# But 'learner' is preceded by L.
# Maybe I should try to read the model as a string if it's mostly JSON?
# But it has binary floats.

# Let's try to assume L is length-prefixed data IF it's not preceded by #.
# No, that's inconsistent.
# What if S is the one that's weird?
# SL... -> S followed by L(length) then data.
# Then what is L alone?
# Let's look at the file content again.
