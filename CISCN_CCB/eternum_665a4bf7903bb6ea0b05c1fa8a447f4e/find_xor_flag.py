def find_xor_flag(data):
    target = b'flag{'
    for i in range(len(data) - len(target)):
        # Assume key length is 1 to 16
        for key_len in range(1, 17):
            key = []
            for j in range(len(target)):
                key.append(data[i+j] ^ target[j])
            
            # Check if key repeats
            is_valid = True
            if key_len < len(target):
                for j in range(key_len, len(target)):
                    if key[j] != key[j % key_len]:
                        is_valid = False
                        break
            
            if is_valid:
                # Potential key found
                real_key = bytes(key[:key_len])
                # Try to decrypt a bit more
                dec = bytes(data[i+j] ^ real_key[j % key_len] for j in range(50))
                if b'flag{' in dec:
                    print(f"Possible XOR flag at offset {hex(i)}, key {real_key.hex()} ({real_key})")
                    print(f"Dec: {dec}")

with open('tcp.pcap', 'rb') as f:
    pcap = f.read()
find_xor_flag(pcap)

with open('kworker_unpacked', 'rb') as f:
    binary = f.read()
find_xor_flag(binary)
