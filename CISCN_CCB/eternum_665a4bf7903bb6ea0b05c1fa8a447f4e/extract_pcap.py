import dpkt

def extract_payloads(pcap_file):
    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if not isinstance(eth.data, dpkt.ip.IP):
                continue
            ip = eth.data
            if not isinstance(ip.data, dpkt.tcp.TCP):
                continue
            tcp = ip.data
            if tcp.data:
                payload = tcp.data
                if payload.startswith(b'ET3RNUMX'):
                    length = int.from_bytes(payload[8:12], 'big')
                    data = payload[12:12+length]
                    print(f"Packet: {ip.src} -> {ip.dst}, Length: {length}")
                    print(data.hex())

extract_payloads('tcp.pcap')
