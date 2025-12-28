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

payload = bytes.fromhex("c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e")
key = b"eternum_665a4bf7903bb6ea0b05c1fa8a447f4e"
dec = rc4(key, payload)
print(f"Dec: {dec.hex()} | {dec}")
