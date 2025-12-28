import sys

def find_high_entropy_blocks(filename, block_size=16):
    with open(filename, 'rb') as f:
        data = f.read()
    
    for i in range(len(data) - block_size):
        block = data[i:i+block_size]
        # Very simple entropy check: many different bytes
        if len(set(block)) >= block_size - 2:
            # Check if it's printable or not
            if all(32 <= b <= 126 for b in block):
                print(f"Offset: {hex(i)}, Block: {block.decode()}")

find_high_entropy_blocks('kworker_unpacked', 16)
find_high_entropy_blocks('kworker_unpacked', 32)
