from Crypto.PublicKey import ECC
from hashlib import sha512

n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
d = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big") % n

key = ECC.construct(curve='p521', d=d)
pub_x = int(key.pointQ.x)
pub_y = int(key.pointQ.y)

print(f"pub x: {hex(pub_x)}")
print(f"pub y: {hex(pub_y)}")
