import zlib
import base64
import re

with open("payload.txt", "r") as f:
    content = f.read()

# Extract the inner base64 string
# It's inside (_)(b'...')
match = re.search(r"\(_\)\(b'([^']+)'\)", content)
if match:
    inner_b64 = match.group(1)
    # Clean the inner base64 string
    inner_b64 = inner_b64.replace(" ", "").replace("\n", "")
    try:
        # The lambda reverses the string then decodes b64 then decompresses zlib
        decoded = zlib.decompress(base64.b64decode(inner_b64[::-1]))
        print(decoded.decode())
    except Exception as e:
        print(f"Error: {e}")
else:
    print("Inner b64 not found")

