import struct
import re

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

def xor_bytes(a, b):
    return bytes(a[i % len(a)] ^ b[i % len(b)] for i in range(len(b)))

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

# Base keys to try
base_keys = [
    b"ciscn2024",
    bytes.fromhex("665a4bf7903bb6ea0b05c1fa8a447f4e"),
    b"eternum",
    b"ET3RNUMX"
]

for bk in base_keys:
    print(f"Trying Base Key: {bk}")
    for i, p in enumerate(payloads):
        if len(p) < 16: continue
        nonce = p[:16]
        data = p[16:]
        
        # Try derived keys
        derived_keys = [
            bk,
            xor_bytes(bk, nonce),
            bk + nonce,
            nonce + bk
        ]
        
        for dk in derived_keys:
            dec = rc4(dk, data)
            if b'flag' in dec.lower():
                print(f"!!! FOUND FLAG !!! Pkt {i}, Key {dk.hex()}")
                print(f"Dec: {dec}")
            elif dec.startswith(b'\x0a') or dec.startswith(b'\x12'): # Common string field starts
                # Check for printable content
                if all(32 <= b <= 126 for b in dec[2:10]):
                     print(f"Found suspicious dec in Pkt {i}: {dec[:50]}")

print("Search finished.")
