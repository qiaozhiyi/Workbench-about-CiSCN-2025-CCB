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

payloads = [
    "c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e"
]

# The hash from the folder name
folder_hash = "665a4bf7903bb6ea0b05c1fa8a447f4e"
keys = [
    folder_hash.encode(),
    bytes.fromhex(folder_hash),
    b"665a4bf7903bb6ea0b05c1fa8a447f4e"
]

for key in keys:
    dec = rc4(key, bytes.fromhex(payloads[0]))
    print(f"Key: {key.hex() if isinstance(key, bytes) else key}, Dec: {dec.hex()} | {dec}")
