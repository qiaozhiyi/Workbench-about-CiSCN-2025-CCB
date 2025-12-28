import zlib
import base64
import re

def decode_nested(encoded_str):
    _ = lambda __ : zlib.decompress(base64.b64decode(__[::-1]))
    return (_(encoded_str.encode()))

with open("payload.txt", "r") as f:
    content = f.read()

# Extract the outer base64 string
outer_match = re.search(r"b64decode\('([^']+)'\)", content)
if outer_match:
    outer_b64 = outer_match.group(1)
    decoded_outer = base64.b64decode(outer_b64).decode()
    print("Decoded outer script:")
    print(decoded_outer)

    # Extract the inner base64 string
    inner_match = re.search(r"b'([^']+)'", decoded_outer)
    if inner_match:
        inner_b64 = inner_match.group(1)
        # Clean the inner base64 string
        inner_b64 = inner_b64.replace(" ", "").replace("\n", "")
        print("\nDecoded inner script:")
        try:
            print(decode_nested(inner_b64).decode())
        except Exception as e:
            print(f"Error decoding inner: {e}")
else:
    print("Could not find outer base64")
