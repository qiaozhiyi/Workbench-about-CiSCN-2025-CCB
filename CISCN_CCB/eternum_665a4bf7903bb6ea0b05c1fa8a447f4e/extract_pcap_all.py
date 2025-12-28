import struct

def parse_pcap(filename):
    with open(filename, 'rb') as f:
        header = f.read(24)
        if not header: return
        
        while True:
            pkt_header = f.read(16)
            if not pkt_header: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
            pkt_data = f.read(incl_len)
            
            # Ethernet header (14 bytes)
            # IP header (starts at 14)
            ip_header = pkt_data[14:34]
            if len(ip_header) < 20: continue
            
            protocol = ip_header[9]
            if protocol != 6: continue
            
            ihl = (ip_header[0] & 0x0F) * 4
            tcp_start = 14 + ihl
            tcp_header = pkt_data[tcp_start:tcp_start+20]
            if len(tcp_header) < 20: continue
            
            doff = (tcp_header[12] >> 4) * 4
            payload = pkt_data[tcp_start + doff:]
            
            if payload.startswith(b'ET3RNUMX'):
                length = struct.unpack('>I', payload[8:12])[0]
                data = payload[12:12+length]
                src = ".".join(map(str, ip_header[12:16]))
                dst = ".".join(map(str, ip_header[16:20]))
                print(f"SRC:{src} DST:{dst} LEN:{length} DATA:{data.hex()}")

parse_pcap('tcp.pcap')
