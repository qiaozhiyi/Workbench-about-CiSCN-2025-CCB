import struct

def rc4_stream(key, payloads):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    results = []
    for data in payloads:
        out = []
        for byte in data:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            out.append(byte ^ S[(S[i] + S[j]) % 256])
        results.append(bytes(out))
    return results

def get_payloads(filename, src_ip):
    with open(filename, 'rb') as f:
        pcap = f.read()
    
    # Very simple pcap parsing
    payloads = []
    idx = 0
    while True:
        idx = pcap.find(b'ET3RNUMX', idx)
        if idx == -1: break
        
        # Check source IP in IP header
        # IP header starts 20-34 bytes before ET3RNUMX usually
        # Let's find the IP header by looking for 0x45 (IPv4)
        ip_idx = pcap.rfind(b'\x45', 0, idx)
        if ip_idx != -1:
            src = ".".join(map(str, pcap[ip_idx+12:ip_idx+16]))
            if src == src_ip:
                length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
                payloads.append(pcap[idx+12 : idx+12+length])
        idx += 1
    return payloads

client_ip = "192.168.8.178"
payloads = get_payloads('tcp.pcap', client_ip)

keys = [
    b"665a4bf7903bb6ea0b05c1fa8a447f4e",
    b"eternum",
    b"ET3RNUMX",
    b"DH4Y9K23Y"
]

for key in keys:
    print(f"Key: {key}")
    decs = rc4_stream(key, payloads)
    for i, d in enumerate(decs):
        print(f"  Pkt {i}: {d[:20].hex()} | {d[:20]}")
