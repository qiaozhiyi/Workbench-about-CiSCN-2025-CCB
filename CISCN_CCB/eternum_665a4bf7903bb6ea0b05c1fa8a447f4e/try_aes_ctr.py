from Crypto.Cipher import AES
import struct

def decrypt_aes_ctr(key, nonce, data):
    # AES-CTR in Go often uses 16-byte nonce/iv
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce[:8], initial_value=nonce[8:])
    try:
        return cipher.decrypt(data)
    except:
        return None

def decrypt_aes_ctr_go(key, nonce, data):
    # Go's cipher.NewCTR(block, iv)
    cipher = AES.new(key, AES.MODE_CTR, nonce=b"", initial_value=nonce)
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

key = bytes.fromhex("665a4bf7903bb6ea0b05c1fa8a447f4e")

for i, (nonce, data) in enumerate(payloads):
    dec = decrypt_aes_ctr_go(key, nonce, data)
    if dec and (dec.startswith(b'\x08') or b'flag' in dec):
        print(f"FOUND! Pkt {i}, Dec: {dec}")
