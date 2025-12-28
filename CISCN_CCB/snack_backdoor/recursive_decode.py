import zlib
import base64
import re

def decode_layer(code):
    _ = lambda __ : zlib.decompress(base64.b64decode(__[::-1]))
    match = re.search(r"\(_\)\(b'([^']+)'\)", code)
    if not match:
        return None
    inner_b64 = match.group(1).replace(" ", "").replace("\n", "")
    try:
        return (_(inner_b64)).decode()
    except Exception as e:
        print(f"Error: {e}")
        return None

with open("backdoor_extracted.py", "r") as f:
    current_code = f.read()

iteration = 1
while True:
    print(f"Decoding layer {iteration}...")
    next_code = decode_layer(current_code)
    if next_code is None:
        print("No more layers found or error occurred.")
        break
    current_code = next_code
    iteration += 1
    if iteration > 100: # Safety break
        break

with open("backdoor_final.py", "w") as f:
    f.write(current_code)

print(f"Final code saved to backdoor_final.py (after {iteration-1} iterations)")
