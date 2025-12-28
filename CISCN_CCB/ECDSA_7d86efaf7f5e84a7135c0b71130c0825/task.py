#!/usr/bin/env python3
from ecdsa import SigningKey, NIST521p
from hashlib import sha512
from Crypto.Util.number import long_to_bytes
import random
import binascii
import sys

digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
curve_order = NIST521p.order
priv_int = digest_int % curve_order
priv_bytes = long_to_bytes(priv_int, 66)
sk = SigningKey.from_string(priv_bytes, curve=NIST521p)
vk = sk.verifying_key

f_pub = open("public.pem", "wb")
f_pub.write(vk.to_pem())
f_pub.close()

def nonce(i):
    seed = sha512(b"bias" + bytes([i])).digest()
    k = int.from_bytes(seed, "big")
    return k

msgs = [b"message-" + bytes([i]) for i in range(60)]
sigs = []

for i, msg in enumerate(msgs):
    k = nonce(i)
    sig = sk.sign(msg, k=k)
    sigs.append((binascii.hexlify(msg).decode(), binascii.hexlify(sig).decode()))

f_sig = open("signatures.txt", "w")
for m, s in sigs:
    f_sig.write("%s:%s\n" % (m, s))
f_sig.close()
