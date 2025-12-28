from Crypto.Cipher import AES
import struct

def decrypt_aes_cbc(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        return cipher.decrypt(data)
    except:
        return None

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()

payloads = []
idx = 0
while True:
    idx = pcap.find(b'ET3RNUMX', idx)
    if idx == -1: break
    length = struct.unpack('>I', pcap[idx+8:idx+12])[0]
    p = pcap[idx+12 : idx+12+length]
    if len(p) >= 16:
        payloads.append((p[:16], p[16:]))
    idx += 1

key = (b"DH4Y9K23Y" + b"\x00"*16)[:16]

for i, (iv, data) in enumerate(payloads):
    dec = decrypt_aes_cbc(key, iv, data)
    if dec and (dec.startswith(b'\x08') or b'flag' in dec):
        print(f"FOUND! Pkt {i}, Dec: {dec}")
