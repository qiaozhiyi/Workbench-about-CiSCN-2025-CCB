import struct
import re

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

payloads = [
    bytes.fromhex("c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e")
]

def is_likely_proto(data):
    # Protobuf often starts with field 1 or 2
    if len(data) < 2: return False
    # Common starts: 08 (field 1, varint), 12 (field 2, bytes), 1a (field 3, bytes)
    return data[0] in [0x08, 0x12, 0x1a]

with open('kworker_unpacked', 'rb') as f:
    data = f.read()
    
# Find all sequences of 8-32 printable characters
strings = re.findall(b'[a-zA-Z0-9]{8,32}', data)
seen = set()

for s in strings:
    if s in seen: continue
    seen.add(s)
    dec = rc4(s, payloads[0])
    if is_likely_proto(dec):
        print(f"Found potential key: {s}, Dec: {dec.hex()}")

# Also try "eternum" variations
for s in [b"eternum", b"ET3RNUMX", b"Eternal", b"resistance"]:
    dec = rc4(s, payloads[0])
    if is_likely_proto(dec):
        print(f"Manual key: {s}, Dec: {dec.hex()}")
