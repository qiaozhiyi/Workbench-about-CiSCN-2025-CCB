import binascii
from hashlib import sha1, sha512

n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
d = 0xe109b2b0a3d9acdd5f642935b2d1539d79583685a92959e929d8a9c1aa8965ee33bd3dfc9e2d37c147d0d1ab17016ba28a2840bb030d2dc9354b1da1209b3cf1

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

with open("signatures.txt", "r") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    msg_hex, sig_hex = line.strip().split(":")
    msg = binascii.unhexlify(msg_hex)
    sig = binascii.unhexlify(sig_hex)
    r = int.from_bytes(sig[:66], "big")
    s = int.from_bytes(sig[66:], "big")
    
    k = nonce(i)
    z = int.from_bytes(sha1(msg).digest(), "big")
    
    if (k * s) % n != (z + r * d) % n:
        print(f"Signature {i} is INVALID!")
# No news is good news
