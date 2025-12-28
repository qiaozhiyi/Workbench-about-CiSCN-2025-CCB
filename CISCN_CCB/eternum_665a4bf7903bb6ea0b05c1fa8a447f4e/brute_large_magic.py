import struct

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

# Large payload content
with open('packet_2048.bin', 'rb') as f:
    payload = f.read()

# Try all strings from binary again, but check for zip or other magics
import re
with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary)
seen = set()

for s in strings:
    if s in seen: continue
    seen.add(s)
    dec = rc4(s, payload)
    # Zip magic
    if dec.startswith(b'PK\x03\x04'):
        print(f"FOUND ZIP! Key: {s}")
        with open('found.zip', 'wb') as f2:
            f2.write(dec)
    # Gzip magic
    elif dec.startswith(b'\x1f\x8b\x08'):
        print(f"FOUND GZIP! Key: {s}")
    # ELF magic
    elif dec.startswith(b'\x7fELF'):
        print(f"FOUND ELF! Key: {s}")
    # Protobuf
    elif dec[0] == 0x08 and 1 <= dec[1] <= 6:
        # Check if it contains 'flag'
        if b'flag' in dec:
            print(f"FOUND FLAG IN PROTO! Key: {s}, Dec: {dec}")
