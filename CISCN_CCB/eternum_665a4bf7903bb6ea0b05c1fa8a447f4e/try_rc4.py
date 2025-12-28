import struct

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []
    
    # KSA
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
        
    # PRGA
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
        
    return bytes(out)

# Packets from extract_pcap_simple.py
payloads = [
    "c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e",
    "c8250252aab6d388bd562cee09f4ce88dad989dcc4d50f400b2c2c99b0e667ecc635b0d26fd5f3fafab1c67a883bc380c3f726",
    "d70228e9e42faa665cd6fad4f3a943ae4d16464a94ac2fa7976300c1db22d78caec13b77c9b82b8c3fc92732e96a8389ed2992f7"
]

keys = [b"eternum", b"Eternum", b"ETERNUX", b"ET3RNUMX", b"Eternal control, eternal resistance"]

for key in keys:
    print(f"Trying key: {key}")
    for p in payloads:
        dec = rc4(key, bytes.fromhex(p))
        print(f"  {dec.hex()} | {dec[:16]}")
