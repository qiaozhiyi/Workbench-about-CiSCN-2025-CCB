def xor_key(data, key):
    out = []
    for i in range(len(data)):
        out.append(data[i] ^ key[i % len(key)])
    return bytes(out)

payload = bytes.fromhex("c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e")
key = b"ET3RNUMX"
dec = xor_key(payload, key)
print(f"XOR with ET3RNUMX: {dec.hex()} | {dec}")
