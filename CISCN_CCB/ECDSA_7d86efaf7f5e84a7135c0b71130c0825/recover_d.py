import binascii
from hashlib import sha512

n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

# From signatures.txt
# 6d6573736167652d00:01a76ff5e0a4490f314ab2a0650d4e9d6955fb154c39eeec2700fefac7b4aeef1230142b1466809d30bc61f32d9ce44757b604b09e211753032c28b64ef9327db44d00c9545bcb3def28828a7424c03d5b688b7ea0581372d9efc417724ab6624244dae9283789a7d7a2f8c2f820fc032dec0c3c2363f2b759e81248f75110344cd13c26
msg0_hex = "6d6573736167652d00"
sig0_hex = "01a76ff5e0a4490f314ab2a0650d4e9d6955fb154c39eeec2700fefac7b4aeef1230142b1466809d30bc61f32d9ce44757b604b09e211753032c28b64ef9327db44d00c9545bcb3def28828a7424c03d5b688b7ea0581372d9efc417724ab6624244dae9283789a7d7a2f8c2f820fc032dec0c3c2363f2b759e81248f75110344cd13c26"
msg0 = binascii.unhexlify(msg0_hex)
sig0 = binascii.unhexlify(sig0_hex)

r = int.from_bytes(sig0[:66], "big")
s = int.from_bytes(sig0[66:], "big")

k = nonce(0)

# hash of message
z_bytes = sha512(msg0).digest()
z = int.from_bytes(z_bytes, "big")

# d = r^-1 * (s*k - z) mod n
d = (pow(r, -1, n) * (s * k - z)) % n

print(f"Recovered d: {hex(d)}")

# Compare with the one from task.py
digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
priv_int = digest_int % n
print(f"Template d:  {hex(priv_int)}")

if d == priv_int:
    print("MATCH!")
else:
    print("NO MATCH! The private key is different.")

