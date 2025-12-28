import binascii
from hashlib import sha512

n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

# Recovered d from sig 0
d = 0x1b42a5acbce598cba9a08a9b2f0e522d399273741dd19a1bbaeac864c401e473f1ec452bbce8685fc8c747fcde9954bb511f15c64d05cfec669f38bd60bc0beaffe

# Check against sig 1
# 6d6573736167652d01:0048955974b1e4270bc53524e878c60e8664e2a71ae031deb7caba819024cf7ff64d2ec4036a902b1d801c84751c3f97d88f85f56b6451fb4fe7f6fcb8dec09d52d2010c44706874ea123630deb0ff48176cae1359a29161c5da30d47121f1f4432588b4235c78febcea2643a9522099d0a88025382af940a5b8b21c04143f01c8f54656
msg1 = binascii.unhexlify("6d6573736167652d01")
sig1 = binascii.unhexlify("0048955974b1e4270bc53524e878c60e8664e2a71ae031deb7caba819024cf7ff64d2ec4036a902b1d801c84751c3f97d88f85f56b6451fb4fe7f6fcb8dec09d52d2010c44706874ea123630deb0ff48176cae1359a29161c5da30d47121f1f4432588b4235c78febcea2643a9522099d0a88025382af940a5b8b21c04143f01c8f54656")

r1 = int.from_bytes(sig1[:66], "big")
s1 = int.from_bytes(sig1[66:], "big")

k1 = nonce(1)
z1 = int.from_bytes(sha512(msg1).digest(), "big")

# s1 = k1^-1 * (z1 + r1*d) mod n
# k1*s1 = z1 + r1*d mod n
if (k1 * s1) % n == (z1 + r1 * d) % n:
    print("VERIFIED! d is correct.")
else:
    print("FAILED! d is incorrect.")
    print(f"k1*s1 mod n: {(k1 * s1) % n}")
    print(f"z1+r1*d mod n: {(z1 + r1 * d) % n}")

