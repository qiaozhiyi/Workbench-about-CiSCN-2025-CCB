with open('kworker_unpacked', 'rb') as f:
    data = f.read()

key = b"ET3RNUMX"
dec = bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))
if b'flag{' in dec:
    print(f"Found flag! {dec[dec.find(b'flag{'):dec.find(b'flag{')+50]}")
else:
    print("Not found")
