from scapy.all import rdpcap, TCP

packets = rdpcap("shell_download.pcap")
payload = b""
for pkt in packets:
    if pkt.haslayer(TCP) and pkt[TCP].payload:
        if pkt[TCP].sport == 8080:
            payload += bytes(pkt[TCP].payload)

# The payload contains HTTP headers followed by the ZIP file
# HTTP/1.1 200 OK ... \r\n\r\n
if b"\r\n\r\n" in payload:
    zip_data = payload.split(b"\r\n\r\n", 1)[1]
    # The length should be around 4403
    print(f"Extracted zip data length: {len(zip_data)}")
    with open("extracted_shell.zip", "wb") as f:
        f.write(zip_data)
else:
    print("HTTP header end not found")

