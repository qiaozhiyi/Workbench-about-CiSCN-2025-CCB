import binascii

RC4_SECRET = b'v1p3r_5tr1k3_k3y'

def rc4_crypt(data: bytes, key: bytes) -> bytes:
	S = list(range(256))
	j = 0
	for i in range(256):
		j = (j + S[i] + key[i % len(key)]) % 256
		S[i], S[j] = S[j], S[i]
	i = j = 0
	res = bytearray()
	for char in data:
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		S[i], S[j] = S[j], S[i]
		res.append(char ^ S[(S[i] + S[j]) % 256])
	return bytes(res)

data_list = [
    "a2ae330da7846599188b26257a88f10b50790cb47e6a97177e1053c351",
    "a3ab330fb285",
    "a6bc",
    "acad614ef3d82c8445d275713899f04d0d3819fc3726cf57634b189e0e95cc1f93e57656105246251f453a8396a43a6534",
    "acb07e4db7c93ece4bcc37246687ae0649614caa3430ce4b7",
    "bab6694ba3c938e64b8d257b7cccee460f6347f4363ed21c300c099f129b99028eb57408024e1c32061a",
    "e0ac7e52fc996cc2038c2d7a3899ed"
]

for d in data_list:
    try:
        # Clean hex string (remove any trailing & or -)
        d_clean = "".join(c for i, c in enumerate(d) if c in "0123456789abcdefABCDEF")
        if len(d_clean) % 2 != 0:
            d_clean = d_clean[:-1]
        enc_cmd = binascii.unhexlify(d_clean)
        cmd = rc4_crypt(enc_cmd, RC4_SECRET).decode('utf-8', errors='ignore')
        print(f"Data: {d} -> Decrypted: {cmd}")
    except Exception as e:
        print(f"Error decrypting {d}: {e}")
