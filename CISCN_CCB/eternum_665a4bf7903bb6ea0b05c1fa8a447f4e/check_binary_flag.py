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

# If the key is ciscn2024, maybe it's used to decrypt a config in the binary?
# Or maybe the flag is just encrypted in the binary.

with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

# Search for the large block of high-entropy data in binary
# Often at the end of the file.
tail = binary[-10000:]
key = b"ciscn2024"
dec = rc4(key, tail)
if b'flag{' in dec:
    print(f"Flag in tail! {dec[dec.find(b'flag{'):dec.find(b'flag{')+50]}")

# Try XOR with ciscn2024 on the whole binary
dec_xor = bytes(binary[i] ^ key[i % len(key)] for i in range(len(binary)))
if b'flag{' in dec_xor:
    print("Flag in binary XOR!")
