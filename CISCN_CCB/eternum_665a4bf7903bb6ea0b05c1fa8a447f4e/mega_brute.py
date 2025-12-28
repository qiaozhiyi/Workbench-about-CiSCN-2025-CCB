import struct

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()

payloads = []
idx = 0
while True:
    idx = pcap.find(b'ET3RNUMX', idx)
    if idx == -1: break
    length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
    p = pcap[idx+12 : idx+12+length]
    payloads.append(p)
    idx += 1

# Extract all printable strings of length 8-32 from the binary again
import re
with open('kworker_unpacked', 'rb') as f:
    binary = f.read()
    
# More aggressive string extraction
strings = re.findall(b'[a-zA-Z0-9_\-\.]{4,32}', binary)
seen = set()

print(f"Brute forcing {len(strings)} strings...")

for s in strings:
    if s in seen: continue
    seen.add(s)
    for i, p in enumerate(payloads):
        if len(p) < 16: continue
        nonce = p[:16]
        data = p[16:]
        
        # Try some common Go key derivation patterns
        for key in [s, s + nonce, nonce + s]:
            dec = rc4(key, data)
            if b'flag{' in dec:
                print(f"!!! FOUND FLAG !!! Key: {key}, Pkt: {i}")
                print(f"Dec: {dec}")
                exit(0)
