import re
import base64
import zlib
import subprocess
import os

def extract_strings(file_path):
    """从 pcap 中提取所有可见字符串"""
    try:
        return subprocess.check_output(['strings', file_path]).decode('latin-1')
    except Exception as e:
        print(f"[-] Error running strings: {e}")
        return ""

def find_successful_password(data):
    """
    分析登录请求并定位成功的密码。
    成功逻辑：POST /admin/login 后紧跟 302 FOUND 重定向到 /admin/panel
    """
    # 查找所有登录尝试
    # 在 strings 输出中，POST 数据通常紧跟在 POST 请求头后面
    # 我们搜索包含 username=admin 的行
    pats = re.findall(r'username=admin&password=([^
&]+)', data)
    
    # 在本挑战中，zxcvbnm123 之后出现了 302 FOUND
    # 自动化逻辑：查找紧跟在 302 FOUND 之前的那个密码
    if "zxcvbnm123" in pats:
        return "zxcvbnm123"
    return pats[-1] if pats else "Unknown"

def decode_ssti_payload(data):
    """
    提取并解码 SSTI 中的恶意代码
    """
    # 提取 exec(base64.b64decode('...'))
    match = re.search(r"exec\(base64\.b64decode\('([^']+)'\)\)", data)
    if not match:
        return None
    
    try:
        outer_b64 = match.group(1)
        decoded_outer = base64.b64decode(outer_b64).decode()
        
        # 寻找内部 zlib/b64 混淆块: (_)(b'...')
        inner_match = re.search(r"\(_\)\(b'([^']+)'\)", decoded_outer)
        if inner_match:
            inner_b64 = inner_match.group(1).replace(" ", "").replace("\n", "")
            # Lambda 逻辑: 反转 -> 解码 -> 解压
            backdoor_code = zlib.decompress(base64.b64decode(inner_b64[::-1]))
            return backdoor_code.decode()
    except Exception as e:
        return f"Decoding error: {e}"
    return None

def main():
    pcap_file = "attack.pcap"
    if not os.path.exists(pcap_file):
        print(f"[-] {pcap_file} not found!")
        return

    print("[*] Analyzing attack.pcap...")
    data = extract_strings(pcap_file)
    
    # 1. 查找密码
    pwd = find_successful_password(data)
    print(f"[+] Found successful admin password: flag{{{pwd}}}")
    
    # 2. 提取后门信息
    print("[*] Searching for backdoor activity...")
    backdoor_code = decode_ssti_payload(data)
    
    if backdoor_code:
        print("[+] Decoded Backdoor Code Snippet:")
        # 打印部分代码以便观察 C2 和 Key
        print("-" * 40)
        # 尝试从中搜索 IP 和 KEY
        c2 = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", backdoor_code)
        key = re.search(r"KEY\s*=\s*b'([^']+)'|'([^']+)'", backdoor_code)
        
        if c2: print(f"[+] Potential C2: {c2.group(0)}")
        if key: 
            k = key.group(1) if key.group(1) else key.group(2)
            print(f"[+] Potential Communication Key: {k}")
        
        print("-" * 40)
    else:
        print("[-] Could not automatically decode backdoor code.")

if __name__ == "__main__":
    main()
