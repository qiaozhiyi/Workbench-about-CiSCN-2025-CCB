from Crypto.Cipher import AES

def decrypt_aes(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        dec = cipher.decrypt(data)
        return dec
    except:
        return None

with open('packet_2048.bin', 'rb') as f:
    data = f.read()

key = bytes.fromhex("665a4bf7903bb6ea0b05c1fa8a447f4e")
dec = decrypt_aes(data, key)
if dec:
    print(f"Decrypted AES (first 64): {dec[:64].hex()}")
    if b'flag' in dec:
        print(f"Found flag! {dec}")
