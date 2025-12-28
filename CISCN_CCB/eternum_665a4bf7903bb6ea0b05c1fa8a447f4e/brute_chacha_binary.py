import struct
import re

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
    ctx[0:4] = [0x61707865, 0x33322062, 0x646e6137, 0x6b206574]
    ctx[4:12] = struct.unpack('<8I', key)
    ctx[12] = counter
    ctx[13:16] = struct.unpack('<3I', nonce)
    working = list(ctx)
    for _ in range(4):
        chacha_quarter_round(working, 0, 4, 8, 12)
        chacha_quarter_round(working, 1, 5, 9, 13)
        chacha_quarter_round(working, 2, 6, 10, 14)
        chacha_quarter_round(working, 3, 7, 11, 15)
        chacha_quarter_round(working, 0, 5, 10, 15)
        chacha_quarter_round(working, 1, 6, 11, 12)
        chacha_quarter_round(working, 2, 7, 8, 13)
        chacha_quarter_round(working, 3, 4, 9, 14)
    return struct.pack('<16I', *((working[i] + ctx[i]) & 0xffffffff for i in range(16)))

def chacha_decrypt(key, nonce, data):
    out = []
    for i in range(0, len(data), 64):
        block = data[i:i+64]
        keystream = chacha_block(key, nonce, i // 64)
        out.append(bytes(a ^ b for a, b in zip(block, keystream)))
    return b"".join(out)

with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

# Get large payload
with open('tcp.pcap', 'rb') as f:
    pcap = f.read()
    idx = pcap.find(b'ET3RNUMX\x00\x00\x08\x00')
    if idx != -1:
        payload = pcap[idx+12 : idx+12+2048]
        nonce = payload[:12]
        data = payload[12:]
    else:
        payload = None

if payload:
    print("Brute forcing ChaCha8 keys...")
    # Try all 32-byte blocks from binary
    for i in range(len(binary) - 32):
        key = binary[i:i+32]
        # Only try if it looks like a key (not all zeros, etc)
        if len(set(key)) < 10: continue
        dec = chacha_decrypt(key, nonce, data[:100])
        if b'flag{' in dec:
            print(f"FOUND FLAG! Key at {hex(i)}, Dec: {dec}")
            break
else:
    print("Large payload not found")
