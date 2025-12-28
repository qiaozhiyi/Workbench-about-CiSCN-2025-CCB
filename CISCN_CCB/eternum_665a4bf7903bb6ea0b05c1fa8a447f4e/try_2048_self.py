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

with open('packet_2048.bin', 'rb') as f:
    payload = f.read()

key = payload[:16]
data = payload[16:]
dec = rc4(key, data)
print(f"Dec (first 100): {dec[:100]}")
if b'flag' in dec:
    print(f"Found flag! {dec}")
