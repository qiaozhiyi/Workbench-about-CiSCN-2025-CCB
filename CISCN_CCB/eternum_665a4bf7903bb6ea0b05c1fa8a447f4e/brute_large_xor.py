import re

def xor_key(data, key):
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))

with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary)
seen = set()

with open('packet_2048.bin', 'rb') as f:
    payload = f.read()

if payload:
    print("Brute forcing XOR keys on large packet...")
    for s in strings:
        if s in seen: continue
        seen.add(s)
        dec = xor_key(payload, s)
        if b'flag{' in dec:
            print(f"FOUND FLAG! Key: {s}, Dec: {dec}")
            break
