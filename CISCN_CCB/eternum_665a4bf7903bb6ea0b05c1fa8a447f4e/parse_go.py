import struct

def find_pclntab(data):
    # Go 1.2+ pclntab magic
    # 0xfffffffb 0x00 0x00 0x01 0x01 (Go 1.16+)
    # 0xfffffff0 0xfffffffa (Older)
    # Let's search for 0xfffffffb
    idx = data.find(b'\xfb\xff\xff\xff\x00\x00\x01\x01')
    if idx == -1:
        idx = data.find(b'\xf0\xff\xff\xff')
    return idx

def parse_pclntab(data, base_addr=0x400000):
    idx = find_pclntab(data)
    if idx == -1: return None
    
    print(f"pclntab found at offset: {hex(idx)}")
    # Go 1.18+ format:
    # magic (4), _, _, _, count (8), ...
    count = struct.unpack('<Q', data[idx+8 : idx+16])[0]
    print(f"Function count: {count}")
    
    # Names are in a table
    # This is complex to parse fully without knowing the exact Go version.
    # But let's try to find main.main
    main_main_idx = data.find(b'main.main\x00')
    if main_main_idx != -1:
        print(f"main.main string at: {hex(main_main_idx)}")

with open('kworker_unpacked', 'rb') as f:
    data = f.read()

parse_pclntab(data)
