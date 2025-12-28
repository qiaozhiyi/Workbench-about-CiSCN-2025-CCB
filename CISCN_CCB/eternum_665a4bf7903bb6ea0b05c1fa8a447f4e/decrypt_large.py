import struct

def rc4(key, data):
    S = list(range(256))
    j = 0
    out = []
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(out)

# Extract the 2048 byte packet
with open('tcp.pcap', 'rb') as f:
    pcap = f.read()
    # Search for the 2048 byte packet
    # LEN:2048 (0x00000800 in hex)
    # ET3RNUMX is 45 54 33 52 4e 55 4d 58
    # 2048 is 00 00 08 00
    pattern = b'ET3RNUMX\x00\x00\x08\x00'
    idx = pcap.find(pattern)
    if idx != -1:
        payload = pcap[idx+12 : idx+12+2048]
        key = b"DH4Y9K23Y"
        dec = rc4(key, payload)
        print(f"Decrypted (first 100 bytes): {dec[:100].hex()}")
        print(f"Decrypted (as string): {dec[:100]}")
    else:
        print("Packet not found")
