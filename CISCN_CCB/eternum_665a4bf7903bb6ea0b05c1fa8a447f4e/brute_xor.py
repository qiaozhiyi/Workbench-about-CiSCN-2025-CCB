with open('packet_2048.bin', 'rb') as f:
    data = f.read()

for i in range(256):
    dec = bytes(b ^ i for b in data)
    if b'flag{' in dec:
        print(f"Found flag with XOR {hex(i)}: {dec}")
    elif b'flag' in dec:
        print(f"Found potential flag with XOR {hex(i)}")
