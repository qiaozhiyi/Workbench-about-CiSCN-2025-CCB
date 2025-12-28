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

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

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

master_keys = [
    b"ciscn2024",
    bytes.fromhex("665a4bf7903bb6ea0b05c1fa8a447f4e"),
    b"ET3RNUMX",
    b"eternum"
]

for mk in master_keys:
    print(f"Master Key: {mk}")
    for i, (nonce, data) in enumerate(payloads):
        # Key could be XOR or concat
        key = xor_bytes(mk, nonce)
        dec = rc4(key, data)
        if dec.startswith(b'\x08') or b'flag' in dec:
            print(f"  Pkt {i} dec: {dec.hex()} | {dec}")
