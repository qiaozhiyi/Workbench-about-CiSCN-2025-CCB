import struct

def rotate(v, c):
    return ((v << c) & 0xffffffff) | (v >> (32 - c))

def chacha_quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 16)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 12)
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 8)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 7)

def chacha_block(key, nonce, counter):
    ctx = [0] * 16
    ctx[0:4] = [0x61707865, 0x33322062, 0x646e6137, 0x6b206574] # "expand 32-byte k"
    ctx[4:12] = struct.unpack('<8I', key)
    ctx[12] = counter
    ctx[13:16] = struct.unpack('<3I', nonce)
    
    working = list(ctx)
    for _ in range(4): # 8 rounds (4 * 2)
        # Column rounds
        chacha_quarter_round(working, 0, 4, 8, 12)
        chacha_quarter_round(working, 1, 5, 9, 13)
        chacha_quarter_round(working, 2, 6, 10, 14)
        chacha_quarter_round(working, 3, 7, 11, 15)
        # Diagonal rounds
        chacha_quarter_round(working, 0, 5, 10, 15)
        chacha_quarter_round(working, 1, 6, 11, 12)
        chacha_quarter_round(working, 2, 7, 8, 13)
        chacha_quarter_round(working, 3, 4, 9, 14)
        
    return struct.pack('<16I', *((working[i] + ctx[i]) & 0xffffffff for i in range(16)))

def chacha_encrypt(key, nonce, data, rounds=8):
    # This is a simplified version for one block
    keystream = chacha_block(key, nonce, 0)
    return bytes(a ^ b for a, b in zip(data, keystream))

# Packet 1 from client
# LEN:52 DATA:c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e
payload = bytes.fromhex("c96e7de65400a76b2122b0584b544c1d99760e0a2d9e91e81673bf99172ee000e690a58c8431a2fab77bd4a304ed89d5964e872e")
nonce = payload[:12]
data = payload[12:]

key = b"665a4bf7903bb6ea0b05c1fa8a447f4e" # 32 bytes

dec = chacha_encrypt(key, nonce, data)
print(f"Decrypted: {dec.hex()} | {dec}")
