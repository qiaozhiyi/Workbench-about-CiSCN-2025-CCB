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

with open('kworker_unpacked', 'rb') as f:
    binary_data = f.read()

payload = bytes.fromhex("c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e")

# Brute force from strings
strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary_data)
seen = set()

for s in strings:
    if s in seen: continue
    seen.add(s)
    dec = rc4(s, payload)
    # Check for common Protobuf starts
    if dec[0] == 0x08:
        # msg_type is likely 1-6
        if 1 <= dec[1] <= 6:
            print(f"Possible key found! Key: {s}, Dec: {dec.hex()}")
            # Check if there is another field
            if len(dec) > 2 and dec[2] in [0x12, 0x1a]:
                print(f"VERY LIKELY key: {s}, Dec: {dec.hex()}")

# Try different encryption start offsets
for offset in range(16):
    p = payload[offset:]
    for s in [b"eternum", b"ET3RNUMX", b"665a4bf7903bb6ea0b05c1fa8a447f4e"]:
        dec = rc4(s, p)
        if dec[0] == 0x08:
             print(f"Offset {offset} key {s} dec: {dec.hex()}")
