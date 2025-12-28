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

# If Packet 0 is 08 01, what is the key?
# Key length could be 1-16.
def find_key_from_start(payload, start_bytes):
    # payload ^ S-box-output = start_bytes
    # start_bytes ^ S-box-output = payload
    # This is hard because S-box depends on the key.
    # Let's brute force all binary strings again but look for 08 04.
    pass

import re
with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary)
seen = set()

print("Searching for FILE_UPLOAD_REQUEST (08 05)...")
for s in strings:
    if s in seen: continue
    seen.add(s)
    # Check Packet 17
    dec = rc4(s, payloads[17])
    if dec.startswith(b'\x08\x05'):
        print(f"FOUND FILE_UPLOAD_REQUEST! Key: {s}")
        # Proto structure for FileUploadRequest:
        # msg_type: 5 (08 05)
        # file_upload_request: field 2? (12 ??)
        if dec[2] == 0x12:
             print(f"Very likely! Dec: {dec[:100]}")
             if b'flag' in dec:
                  print(f"Flag found in dec!")
