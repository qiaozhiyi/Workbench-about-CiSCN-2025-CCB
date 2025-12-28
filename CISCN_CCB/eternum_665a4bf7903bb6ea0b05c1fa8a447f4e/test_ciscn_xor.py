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
    if len(p) >= 16:
        nonce = p[:16]
        data = p[16:]
        payloads.append((nonce, data))
    idx += 1

mk = b"ciscn2024"
for i, (nonce, data) in enumerate(payloads):
    key = xor_bytes(mk, nonce)
    dec = rc4(key, data)
    print(f"Pkt {i} dec: {dec[:20].hex()} | {dec[:20]}")
