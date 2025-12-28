from Crypto.Cipher import AES
import binascii

# 基础数据
initial_key = "FanAglFanAglOoO!"
target_hex = "d458af702a680ae4d089ce32fc39945d"
ciphertext = binascii.unhexlify(target_hex)

def decrypt(key_str):
    try:
        key_bytes = key_str.encode('utf-8')
        # AES-128 需要 16 字节密钥
        if len(key_bytes) != 16:
            return None
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted = cipher.decrypt(ciphertext)
        return decrypted
    except:
        return None

def solve():
    print("开始尝试可能的 Key...")
    
    # 假设规律是：第 N 个金币把字母表第 N 个位置的字符替换为下一个
    # 或者是 A->B, B->C, C->D ... 这种连续替换
    
    current_key = initial_key
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # 模拟 9 个金币的替换过程 (A->B, B->C, ..., I->J)
    for i in range(10):
        res = decrypt(current_key)
        if res:
            try:
                # 尝试解码，看看是否有意义
                plain = res.decode('utf-8', errors='ignore')
                print(f"金币数 {i} | Key: {current_key} | Result: {plain}")
                if "flag" in plain.lower() or "{" in plain:
                    print("\n" + "!"*20)
                    print(f"找到可能是正确的 Flag: {plain}")
                    print("!"*20)
            except:
                pass
        
        # 模拟下一轮替换：把当前的字符换成下一个
        # 比如第一轮把 A 换成 B，第二轮把 B 换成 C
        old_char = alphabet[i]
        new_char = alphabet[i+1]
        current_key = current_key.replace(old_char, new_char)

if __name__ == "__main__":
    solve()
