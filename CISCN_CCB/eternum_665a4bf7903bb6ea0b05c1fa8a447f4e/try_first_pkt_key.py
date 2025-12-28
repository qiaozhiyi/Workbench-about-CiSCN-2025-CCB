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
    payloads.append(pcap[idx+12 : idx+12+length])
    idx += 1

# Try using the first 16 bytes of the first packet as key for all packets
key = payloads[0][:16]
print(f"Key: {key.hex()}")
for i, p in enumerate(payloads):
    dec = rc4(key, p)
    if b'flag' in dec:
        print(f"Found flag in Pkt {i}! {dec}")
    elif i == 0:
        print(f"Pkt 0 dec: {dec.hex()}")
