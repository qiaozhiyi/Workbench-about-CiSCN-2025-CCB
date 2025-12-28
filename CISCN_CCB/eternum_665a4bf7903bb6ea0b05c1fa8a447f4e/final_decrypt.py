import struct

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    out = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()

payloads = []
idx = 0
while True:
    idx = pcap.find(b'ET3RNUMX', idx)
    if idx == -1: break
    length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
    p = pcap[idx+12 : idx+12+length]
    payloads.append(p)
    idx += 1

key = b"DH4Y9K23Y"
print(f"Decrypting with key: {key}")

for i, p in enumerate(payloads):
    # Nonce is the first 16 bytes? Or no nonce?
    # Based on previous trial, DH4Y9K23Y worked on the WHOLE payload including potential nonce.
    # Wait, let's re-check.
    # In my brute_proto.py, I used: dec = rc4(s, payload)
    # where payload = bytes.fromhex("c96e7de6...")
    # So the key decrypts the WHOLE thing.
    dec = rc4(key, p)
    if b'flag{' in dec:
        print(f"!!! FOUND FLAG !!! Pkt {i}")
        print(f"Dec: {dec}")
    elif i == 17: # The 2048 byte packet
        print(f"Pkt 17 dec (first 100): {dec[:100]}")
        # Search for flag in large packet
        if b'flag' in dec.lower():
             print(f"Potential flag in Pkt 17!")
             # Print around 'flag'
             fidx = dec.lower().find(b'flag')
             print(dec[fidx:fidx+100])

# Try with nonce-skipping just in case
print("\nTrying with nonce skipping (16 bytes)...")
for i, p in enumerate(payloads):
    if len(p) <= 16: continue
    data = p[16:]
    dec = rc4(key, data)
    if b'flag{' in dec:
        print(f"!!! FOUND FLAG (with offset) !!! Pkt {i}")
        print(f"Dec: {dec}")
    elif i == 17:
        print(f"Pkt 17 dec with offset (first 100): {dec[:100]}")
        if b'flag' in dec.lower():
             fidx = dec.lower().find(b'flag')
             print(dec[fidx:fidx+100])
