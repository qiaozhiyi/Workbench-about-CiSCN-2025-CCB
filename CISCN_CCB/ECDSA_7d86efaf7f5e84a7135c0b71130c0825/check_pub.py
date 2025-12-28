from ecdsa import SigningKey, NIST521p, VerifyingKey
from hashlib import sha512
from Crypto.Util.number import long_to_bytes
import binascii

digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
n = NIST521p.order
priv_int = digest_int % n
priv_bytes = long_to_bytes(priv_int, 66)

sk = SigningKey.from_string(priv_bytes, curve=NIST521p)
vk = sk.verifying_key
template_pub = vk.to_pem()

with open("public.pem", "rb") as f:
    actual_pub = f.read()

print("Template Pub PEM:")
print(template_pub.decode())
print("Actual Pub PEM:")
print(actual_pub.decode())

if template_pub == actual_pub:
    print("MATCH!")
else:
    print("NO MATCH!")
