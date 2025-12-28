import struct

def parse_pcap(filename):
    with open(filename, 'rb') as f:
        header = f.read(24)
        if not header: return
        magic, _, _, _, _, _, _ = struct.unpack('<IHHIIII', header)
        
        while True:
            pkt_header = f.read(16)
            if not pkt_header: break
            ts_sec, ts_usec, incl_len, orig_len = struct.unpack('<IIII', pkt_header)
            pkt_data = f.read(incl_len)
            
            # Ethernet header (14 bytes)
            eth_header = pkt_data[:14]
            # IP header (starts at 14)
            ip_header = pkt_data[14:34]
            if len(ip_header) < 20: continue
            
            # Check if it's TCP (protocol 6)
            protocol = ip_header[9]
            if protocol != 6: continue
            
            # IP length
            ihl = (ip_header[0] & 0x0F) * 4
            # TCP header (starts at 14 + ihl)
            tcp_start = 14 + ihl
            tcp_header = pkt_data[tcp_start:tcp_start+20]
            if len(tcp_header) < 20: continue
            
            # TCP data offset
            doff = (tcp_header[12] >> 4) * 4
            payload = pkt_data[tcp_start + doff:]
            
            if payload.startswith(b'ET3RNUMX'):
                length = struct.unpack('>I', payload[8:12])[0]
                data = payload[12:12+length]
                print(f"LEN:{length} DATA:{data.hex()}")

parse_pcap('tcp.pcap')
