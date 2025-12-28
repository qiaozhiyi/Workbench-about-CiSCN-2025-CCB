import struct

def rc4_continuous(key, payloads):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    full_dec = b""
    for data in payloads:
        for byte in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            full_dec += bytes([byte ^ S[(S[i] + S[j]) % 256]])
    return full_dec

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()

def get_payloads(pcap, src_ip):
    payloads = []
    idx = 0
    while True:
        idx = pcap.find(b'ET3RNUMX', idx)
        if idx == -1: break
        # Check src ip (rough check)
        ip_idx = pcap.rfind(b'\x45', 0, idx)
        if ip_idx != -1:
            src = ".".join(map(str, pcap[ip_idx+12:ip_idx+16]))
            if src == src_ip:
                length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
                payloads.append(pcap[idx+12 : idx+12+length])
        idx += 1
    return payloads

client_payloads = get_payloads(pcap, "192.168.8.178")

with open('kworker_unpacked', 'rb') as f:
    binary = f.read()

import re
strings = re.findall(b'[a-zA-Z0-9]{4,32}', binary)
seen = set()

for s in strings:
    if s in seen: continue
    seen.add(s)
    dec = rc4_continuous(s, client_payloads)
    if b'flag{' in dec:
        print(f"FOUND FLAG! Key: {s}, Dec: {dec}")
        break
