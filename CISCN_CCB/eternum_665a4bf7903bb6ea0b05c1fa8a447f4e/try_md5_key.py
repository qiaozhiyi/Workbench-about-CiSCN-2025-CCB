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

# What if the key is derived from the nonce in a more complex way?
# like key = md5(nonce + master_key)
import hashlib

master_key = b"ciscn2024"
for i, p in enumerate(payloads):
    if len(p) < 16: continue
    nonce = p[:16]
    data = p[16:]
    
    key = hashlib.md5(nonce + master_key).digest()
    dec = rc4(key, data)
    if dec.startswith(b'\x08') or b'flag' in dec:
        print(f"Match with MD5(nonce+mk)! Pkt {i}, Dec: {dec[:50]}")

    key = hashlib.md5(master_key + nonce).digest()
    dec = rc4(key, data)
    if dec.startswith(b'\x08') or b'flag' in dec:
        print(f"Match with MD5(mk+nonce)! Pkt {i}, Dec: {dec[:50]}")
