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

import re
with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary)
seen = set()

# Try each packet starting from 08 01, 08 02, etc.
expected = {
    0: b'\x08\x01',
    1: b'\x08\x02',
    2: b'\x08\x01',
    3: b'\x08\x02',
    4: b'\x08\x01'
}

for s in strings:
    if s in seen: continue
    seen.add(s)
    match = True
    for pkt_idx, header in expected.items():
        dec = rc4(s, payloads[pkt_idx][:2])
        if dec != header:
            match = False
            break
    if match:
        print(f"Match found! Key: {s}")
        # Decrypt packet 17
        dec17 = rc4(s, payloads[17])
        if b'flag' in dec17:
            print(f"FOUND FLAG! {dec17}")
            exit(0)
