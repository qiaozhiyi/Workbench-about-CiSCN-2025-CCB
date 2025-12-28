import binascii
from hashlib import sha1, sha256, sha384, sha512

n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

msg0 = binascii.unhexlify("6d6573736167652d00")
sig0 = binascii.unhexlify("01a76ff5e0a4490f314ab2a0650d4e9d6955fb154c39eeec2700fefac7b4aeef1230142b1466809d30bc61f32d9ce44757b604b09e211753032c28b64ef9327db44d00c9545bcb3def28828a7424c03d5b688b7ea0581372d9efc417724ab6624244dae9283789a7d7a2f8c2f820fc032dec0c3c2363f2b759e81248f75110344cd13c26")
r0 = int.from_bytes(sig0[:66], "big")
s0 = int.from_bytes(sig0[66:], "big")
k0 = nonce(0)

msg1 = binascii.unhexlify("6d6573736167652d01")
sig1 = binascii.unhexlify("0048955974b1e4270bc53524e878c60e8664e2a71ae031deb7caba819024cf7ff64d2ec4036a902b1d801c84751c3f97d88f85f56b6451fb4fe7f6fcb8dec09d52d2010c44706874ea123630deb0ff48176cae1359a29161c5da30d47121f1f4432588b4235c78febcea2643a9522099d0a88025382af940a5b8b21c04143f01c8f54656")
r1 = int.from_bytes(sig1[:66], "big")
s1 = int.from_bytes(sig1[66:], "big")
k1 = nonce(1)

hashes = {
    "sha1": sha1,
    "sha256": sha256,
    "sha384": sha384,
    "sha512": sha512
}

for name, hfunc in hashes.items():
    z0 = int.from_bytes(hfunc(msg0).digest(), "big")
    d = (pow(r0, -1, n) * (s0 * k0 - z0)) % n
    
    z1 = int.from_bytes(hfunc(msg1).digest(), "big")
    if (k1 * s1) % n == (z1 + r1 * d) % n:
        print(f"Match found! Hash: {name}")
        print(f"d: {hex(d)}")
        break
else:
    print("No match found for standard hashes.")

