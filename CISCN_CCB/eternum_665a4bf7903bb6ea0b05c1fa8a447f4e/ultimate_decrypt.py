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
all_decrypted = b""

for i, p in enumerate(payloads):
    dec = rc4(key, p)
    print(f"Pkt {i} Type: {dec[1] if len(dec)>1 else '?'}")
    all_decrypted += dec
    if b'flag{' in dec:
        print(f"!!! FOUND FLAG IN PKT {i} !!!")
        print(dec)

if b'flag{' in all_decrypted:
    fidx = all_decrypted.find(b'flag{')
    print(f"Full Flag: {all_decrypted[fidx:all_decrypted.find(b'}', fidx)+1]}")
else:
    print("Flag not found in direct decryption. Trying to see if it's across packets...")
    # Maybe the RC4 state is persistent?
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    curr_i = curr_j = 0
    full_stream_dec = b""
    for p in payloads:
        for byte in p:
            curr_i = (curr_i + 1) % 256
            curr_j = (curr_j + S[curr_i]) % 256
            S[curr_i], S[curr_j] = S[curr_j], S[curr_i]
            full_stream_dec += bytes([byte ^ S[(S[curr_i] + S[curr_j]) % 256]])
    
    if b'flag{' in full_stream_dec:
        print("!!! FOUND FLAG IN STREAM !!!")
        fidx = full_stream_dec.find(b'flag{')
        print(full_stream_dec[fidx:full_stream_dec.find(b'}', fidx)+1])
