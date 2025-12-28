import urllib.parse
import base64
import re
import zlib

with open("full_ssti_payload.txt", "r") as f:
    encoded_payload = f.read()

# URL decode
decoded_payload = urllib.parse.unquote_plus(encoded_payload)

# Extract the first layer base64
match1 = re.search(r"base64\.b64decode\('([^']+)'\)", decoded_payload)
if not match1:
    print("Layer 1 base64 not found")
    exit()

layer1_code = base64.b64decode(match1.group(1)).decode()
print("--- Layer 1 Code ---")
print(layer1_code)

# Extract the second layer base64 inside (_)(b'...')
match2 = re.search(r"\(_\)\(b'([^']+)'\)", layer1_code)
if not match2:
    print("Layer 2 base64 not found")
    exit()

layer2_b64 = match2.group(1)
# The lambda: _ = lambda __ : zlib.decompress(base64.b64decode(__[::-1]))
# It reverses the string, then b64 decodes, then zlib decompresses.
try:
    backdoor_code = zlib.decompress(base64.b64decode(layer2_b64[::-1]))
    with open("backdoor_extracted.py", "wb") as f:
        f.write(backdoor_code)
    print("\n--- Backdoor Code Extracted to backdoor_extracted.py ---")
except Exception as e:
    print(f"Error decoding layer 2: {e}")
