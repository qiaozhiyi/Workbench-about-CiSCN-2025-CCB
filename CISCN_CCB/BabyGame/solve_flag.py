from Crypto.Cipher import AES
import binascii

# 尝试使用发现的长十六进制字符串作为密钥
key = binascii.unhexlify("41A2B017516F6D254E1F002BCCBADD54BE30F8CEC737A0E912B4963B6BA74460")
ciphertext_hex = "d458af702a680ae4d089ce32fc39945d"

def solve():
    try:
        ciphertext = binascii.unhexlify(ciphertext_hex)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        
        print("\n" + "="*30)
        print(f"密钥 (Hex): {key.hex()}")
        print(f"解密后的十六进制: {decrypted.hex()}")
        try:
            print(f"尝试 UTF-8 解码: {decrypted.decode('utf-8')}")
        except:
            print("无法进行 UTF-8 解码")
        print("="*30 + "\n")
    except Exception as e:
        print(f"解密失败: {e}")

if __name__ == "__main__":
    solve()

