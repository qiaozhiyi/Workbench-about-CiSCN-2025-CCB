def brute_xor_pcap(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    target = b'flag{'
    for i in range(len(data) - 100):
        # Try XOR with a fixed key from the binary
        pass

# Actually, let's try to decrypt the 2048 byte packet with all strings from the binary as RC4 keys
import re
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

with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary)
seen = set()

# Get the large packet
with open('tcp.pcap', 'rb') as f:
    pcap = f.read()
    idx = pcap.find(b'ET3RNUMX\x00\x00\x08\x00')
    if idx != -1:
        large_payload = pcap[idx+12 : idx+12+2048]
    else:
        large_payload = None

if large_payload:
    print("Large payload found. Brute forcing RC4 keys...")
    for s in strings:
        if s in seen: continue
        seen.add(s)
        dec = rc4(s, large_payload)
        if b'flag{' in dec:
            print(f"FOUND FLAG! Key: {s}, Dec: {dec}")
            break
else:
    print("Large payload not found")
