import struct

def find_pclntab(data):
    # Go 1.18+ pclntab magic: 0xfffffff0
    # Actually, let's just search for the magic
    magics = [b'\xfb\xff\xff\xff', b'\xf0\xff\xff\xff', b'\xf1\xff\xff\xff', b'\xf2\xff\xff\xff']
    for magic in magics:
        idx = data.find(magic)
        if idx != -1:
            return idx, magic
    return -1, None

def parse_go_symbols(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    idx, magic = find_pclntab(data)
    if idx == -1:
        print("pclntab not found")
        return
    
    print(f"Found pclntab at {hex(idx)} with magic {magic.hex()}")
    
    # Simple search for main.main string and then find the pointer to it
    main_main_str = b'main.main\x00'
    str_idx = data.find(main_main_str)
    if str_idx == -1:
        print("main.main string not found")
        return
    
    print(f"main.main string at {hex(str_idx)}")
    
    # In Go pclntab, the function table contains offsets to function structures.
    # Each function structure contains an offset to the name string.
    # This is version dependent.
    
    # Let's try to find all main. functions
    for m in re.finditer(b'main\.[a-zA-Z0-9_]+', data):
        print(f"Found symbol: {m.group()} at {hex(m.start())}")

import re
parse_go_symbols('kworker_unpacked')
