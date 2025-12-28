from pwn import *
import sys
import time

if len(sys.argv) != 3:
    print("Usage: python3 submit.py <HOST> <PORT>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

context.log_level = 'info'

try:
    conn = remote(HOST, PORT)
    
    # Receive the initial banner
    conn.recvuntil(b"Waiting for CSV Data Stream (End with 'EOF')...")
    print("[*] Server ready. Preparing data...")

    # Read the file
    with open('fake_ledger.csv', 'r') as f:
        data = f.read().strip()

    print(f"[*] Sending CSV data ({len(data)} characters)...")
    
    # Send the CSV content
    conn.send(data.encode())
    conn.send(b"\n") # Ensure data ends with newline
    
    time.sleep(0.5)
    
    # Send EOF
    print("[*] Sending EOF...")
    conn.send(b"EOF\n")
    
    print("[*] Waiting for server evaluation...")
    
    # Start receiving
    # Use a longer timeout for the final response as model evaluation takes time
    while True:
        try:
            chunk = conn.recv(4096, timeout=15)
            if not chunk:
                print("\n[*] Connection closed by server.")
                break
            print(chunk.decode(errors='ignore'), end='')
            if b'}' in chunk:
                break
        except EOFError:
            print("\n[*] EOF encountered.")
            break
        except Exception as e:
            print(f"\n[*] Receive timed out or error: {e}")
            break
            
    conn.close()

except Exception as e:
    print(f"[-] Error: {e}")