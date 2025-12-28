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

keys = [
    b"OmPgRox8DEDC",
    b"SgCNV65A",
    b"Eto2aNcXC",
    b"BpN2f4iz30D",
    b"P8SvvwkN2BqnC",
    b"LNWePc3I37NtE",
    b"Lpq0vGWwNbmU",
    b"QbKVT1hamykHV"
]

for key in keys:
    dec = rc4(key, bytes.fromhex(payloads[0]))
    print(f"Key: {key}, Dec: {dec.hex()}")
