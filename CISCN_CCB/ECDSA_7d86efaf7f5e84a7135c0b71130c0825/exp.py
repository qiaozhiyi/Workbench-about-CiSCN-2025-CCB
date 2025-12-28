import binascii
from hashlib import sha1, sha512

# NIST521p 曲线的阶 n
n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449

def get_nonce(i):
    """根据 task.py 中的逻辑重新生成随机数 k"""
    seed = sha512(b"bias" + bytes([i])).digest()
    return int.from_bytes(seed, "big")

def solve():
    # 读取第一条签名数据
    try:
        with open("signatures.txt", "r") as f:
            first_line = f.readline().strip()
    except FileNotFoundError:
        print("[-] signatures.txt not found!")
        return
    
    msg_hex, sig_hex = first_line.split(":")
    msg = binascii.unhexlify(msg_hex)
    sig = binascii.unhexlify(sig_hex)
    
    # ECDSA P-521 签名中 r 和 s 各占 66 字节 (521 bits -> 66 bytes)
    r = int.from_bytes(sig[:66], "big")
    s = int.from_bytes(sig[66:], "big")
    
    # 获取索引为 0 的随机数 k
    k = get_nonce(0)
    
    # 消息哈希 z (经过验证该题签名时对消息使用了 sha1)
    z = int.from_bytes(sha1(msg).digest(), "big")
    
    # 根据公式 d = r^-1 * (s*k - z) mod n 恢复私钥
    # 因为 s = k^-1 * (z + r*d) mod n
    try:
        r_inv = pow(r, -1, n)
        d = (r_inv * (s * k - z)) % n
        
        print(f"[+] Recovered Private Key (d): {hex(d)}")
        
        # 验证是否与 task.py 中的生成逻辑匹配
        template_d = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big") % n
        if d == template_d:
            print("[!] Match found! The recovered key matches the task template.")
            print(f"[!] Flag: flag{{{hex(d)[2:]}}}")
        else:
            print("[-] Warning: Recovered d does not match the template calculation.")
            print(f"[?] Possible Flag: flag{{{hex(d)[2:]}}}")
            
    except ValueError:
        print("[-] Error: r is not invertible modulo n.")

if __name__ == "__main__":
    solve()
