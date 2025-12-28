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
    ctx[0:4] = [0x61707865, 0x33322062, 0x646e6137, 0x6b206574]
    ctx[4:12] = struct.unpack('<8I', key)
    ctx[12] = counter
    ctx[13:16] = struct.unpack('<3I', nonce)
    
    working = list(ctx)
    for _ in range(4): # ChaCha8
        chacha_quarter_round(working, 0, 4, 8, 12)
        chacha_quarter_round(working, 1, 5, 9, 13)
        chacha_quarter_round(working, 2, 6, 10, 14)
        chacha_quarter_round(working, 3, 7, 11, 15)
        chacha_quarter_round(working, 0, 5, 10, 15)
        chacha_quarter_round(working, 1, 6, 11, 12)
        chacha_quarter_round(working, 2, 7, 8, 13)
        chacha_quarter_round(working, 3, 4, 9, 14)
        
    return struct.pack('<16I', *((working[i] + ctx[i]) & 0xffffffff for i in range(16)))

def chacha_decrypt(key, payloads):
    results = []
    for p in payloads:
        if len(p) < 12: continue
        nonce = p[:12]
        data = p[12:]
        keystream = chacha_block(key, nonce, 0)
        results.append(bytes(a ^ b for a, b in zip(data, keystream)))
    return results

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()

payloads = []
idx = 0
while True:
    idx = pcap.find(b'ET3RNUMX', idx)
    if idx == -1: break
    length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
    payloads.append(pcap[idx+12 : idx+12+length])
    idx += 1

# Key could be MD5 of ciscn2024 repeated
key_md5 = bytes.fromhex("665a4bf7903bb6ea0b05c1fa8a447f4e")
keys = [
    key_md5 + key_md5,
    b"ciscn2024" * 4,
    b"eternum" + b"\x00"*25,
    b"ET3RNUMX" * 4
]

for key in keys:
    print(f"Key: {key.hex()}")
    decs = chacha_decrypt(key, payloads)
    for d in decs:
        if d.startswith(b'\x08') or b'flag' in d:
            print(f"  Possible dec: {d.hex()} | {d}")
