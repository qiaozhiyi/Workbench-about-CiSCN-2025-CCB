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

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()

payloads = []
idx = 0
while True:
    idx = pcap.find(b'ET3RNUMX', idx)
    if idx == -1: break
    length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
    payloads.append(pcap[idx+12 : idx+12+length])
    idx += 1

with open('kworker_unpacked', 'rb') as f:
    binary_data = f.read()

strings = re.findall(b'[a-zA-Z0-9]{8,32}', binary_data)
seen = set()

for s in strings:
    if s in seen: continue
    seen.add(s)
    for p in payloads:
        dec = rc4(s, p)
        if b'flag{' in dec:
            print(f"Found flag! Key: {s}, Pkt: {dec}")
        elif b'flag' in dec:
            # Check if it's really a flag
            if b'flag{' in dec.lower():
                 print(f"Found potential flag! Key: {s}, Pkt: {dec}")

print("Search finished.")
