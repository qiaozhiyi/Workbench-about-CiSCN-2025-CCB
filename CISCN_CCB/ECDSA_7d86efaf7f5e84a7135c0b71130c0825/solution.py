from ecdsa import SigningKey, NIST521p
from hashlib import sha512
from Crypto.Util.number import long_to_bytes
import binascii

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
curve_order = NIST521p.order
priv_int = digest_int % curve_order

print(f"Calculated priv_int: {hex(priv_int)}")

# Verify the first signature
# 6d6573736167652d00:01a76ff5e0a4490f314ab2a0650d4e9d6955fb154c39eeec2700fefac7b4aeef1230142b1466809d30bc61f32d9ce44757b604b09e211753032c28b64ef9327db44d00c9545bcb3def28828a7424c03d5b688b7ea0581372d9efc417724ab6624244dae9283789a7d7a2f8c2f820fc032dec0c3c2363f2b759e81248f75110344cd13c26
msg0_hex = "6d6573736167652d00"
sig0_hex = "01a76ff5e0a4490f314ab2a0650d4e9d6955fb154c39eeec2700fefac7b4aeef1230142b1466809d30bc61f32d9ce44757b604b09e211753032c28b64ef9327db44d00c9545bcb3def28828a7424c03d5b688b7ea0581372d9efc417724ab6624244dae9283789a7d7a2f8c2f820fc032dec0c3c2363f2b759e81248f75110344cd13c26"

msg0 = binascii.unhexlify(msg0_hex)
sig0 = binascii.unhexlify(sig0_hex)

priv_bytes = long_to_bytes(priv_int, 66)
sk = SigningKey.from_string(priv_bytes, curve=NIST521p)
vk = sk.verifying_key

k0 = nonce(0)
# Re-sign message 0 with k0
expected_sig0 = sk.sign(msg0, k=k0)
expected_sig0_hex = binascii.hexlify(expected_sig0).decode()

print(f"Expected sig0: {expected_sig0_hex}")
print(f"Actual sig0:   {sig0_hex}")

if sig0_hex == expected_sig0_hex:
    print("Private key matches signatures!")
else:
    print("Private key does NOT match signatures.")

