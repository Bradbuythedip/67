import hashlib
import base58
from datetime import datetime
import threading
import queue
import time
from coincurve import PrivateKey
import os
from multiprocessing import cpu_count

# Constants
TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
BASE_VALUE = 0x16230cfcfa9
RANGE_PER_THREAD = 1_000_000  # How many values each thread checks before reporting
THREAD_COUNT = 28  # Number of threads to use

# Queues for thread communication
result_queue = queue.Queue()
progress_queue = queue.Queue()

def sha256(hex_str):
    return hashlib.sha256(bytes.fromhex(hex_str) if isinstance(hex_str, str) else hex_str).digest()

def generate_bitcoin_address(public_key_bytes, compressed=True):
    """Generate Bitcoin address from public key bytes"""
    # SHA256 + RIPEMD160
    sha256_hash = sha256(public_key_bytes)
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    
    # Add version byte (0x00 for mainnet)
    version_ripemd160_hash = b'\x00' + ripemd160_hash.digest()
    
    # Double SHA256 for checksum
    double_sha = sha256(sha256(version_ripemd160_hash))
    
    # Add first 4 bytes as checksum
    binary_addr = version_ripemd160_hash + double_sha[:4]
    
    # Convert to base58
    address = base58.b58encode(binary_addr).decode()
    
    return address

def process_private_key(private_key_int):
    """Process a single private key value"""
    try:
        # Convert to bytes (32 bytes, big-endian)
        private_key_bytes = private_key_int.to_bytes(32, byteorder='big')
        
        # Generate key pair using coincurve (faster than python-ecdsa)
        private_key = PrivateKey(private_key_bytes)
        public_key = private_key.public_key
        
        # Get compressed and uncompressed public keys
        public_key_compressed = public_key.format(compressed=True)
        public_key_uncompressed = public_key.format(compressed=False)
        
        # Generate addresses
        address_compressed = generate_bitcoin_address(public_key_compressed, True)
        address_uncompressed = generate_bitcoin_address(public_key_uncompressed, False)
        
        return private_key_int, address_compressed, address_uncompressed
        
    except Exception as e:
        return None

def search_range(start_value, range_size, thread_id):
    """Search a range of values for the target address"""
    end_value = start_value + range_size
    current_value = start_value
    last_report_time = time.time()
    keys_checked = 0
    
    while current_value < end_value:
        # Process current value
        result = process_private_key(current_value)
        if result:
            priv_key, addr_comp, addr_uncomp = result
            
            # Check if either address matches
            if addr_comp == TARGET_ADDRESS or addr_uncomp == TARGET_ADDRESS:
                result_queue.put(('FOUND', priv_key, addr_comp, addr_uncomp))
                return
        
        # Update progress
        keys_checked += 1
        if keys_checked % 1000 == 0:
            current_time = time.time()
            if current_time - last_report_time >= 10:  # Report every 10 seconds
                progress_queue.put((thread_id, current_value, keys_checked))
                last_report_time = current_time
                keys_checked = 0
        
        current_value += 1

def progress_monitor():
    """Monitor and display progress from all threads"""
    thread_progress = {}
    start_time = time.time()
    
    while True:
        try:
            thread_id, current_value, keys_checked = progress_queue.get(timeout=1)
            thread_progress[thread_id] = (current_value, keys_checked)
            
            # Calculate and display overall progress
            elapsed_time = time.time() - start_time
            total_keys = sum(checked for _, checked in thread_progress.values())
            keys_per_second = total_keys / elapsed_time if elapsed_time > 0 else 0
            
            print(f"\nProgress Report (Elapsed: {elapsed_time:.1f}s)")
            print(f"Keys checked: {total_keys:,}")
            print(f"Speed: {keys_per_second:.2f} keys/s")
            print(f"Current thread ranges:")
            for tid, (curr_val, _) in thread_progress.items():
                print(f"Thread {tid}: 0x{curr_val:x}")
            
        except queue.Empty:
            continue
        except Exception as e:
            print(f"Error in progress monitor: {str(e)}")
            break

def main():
    print(f"Starting puzzle 67 scanner with {THREAD_COUNT} threads")
    print(f"Target address: {TARGET_ADDRESS}")
    print(f"Base value: 0x{BASE_VALUE:x}")
    print(f"Range per thread: {RANGE_PER_THREAD:,}")
    
    # Start progress monitor
    monitor_thread = threading.Thread(target=progress_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Start search threads
    threads = []
    for i in range(THREAD_COUNT // 2):
        # Positive direction
        start_pos = BASE_VALUE + (i * RANGE_PER_THREAD)
        t_pos = threading.Thread(target=search_range, 
                               args=(start_pos, RANGE_PER_THREAD, f"pos_{i}"))
        threads.append(t_pos)
        t_pos.start()
        
        # Negative direction
        start_neg = BASE_VALUE - ((i + 1) * RANGE_PER_THREAD)
        t_neg = threading.Thread(target=search_range, 
                               args=(start_neg, RANGE_PER_THREAD, f"neg_{i}"))
        threads.append(t_neg)
        t_neg.start()
    
    # Monitor for results
    try:
        while any(t.is_alive() for t in threads):
            try:
                msg_type, *data = result_queue.get(timeout=1)
                if msg_type == 'FOUND':
                    priv_key, addr_comp, addr_uncomp = data
                    print("\nMATCH FOUND!")
                    print(f"Private Key: 0x{priv_key:x}")
                    print(f"Private Key (decimal): {priv_key}")
                    print(f"Compressed Address: {addr_comp}")
                    print(f"Uncompressed Address: {addr_uncomp}")
                    
                    # Save to file
                    with open('puzzle67_solution.txt', 'w') as f:
                        f.write(f"Private Key (hex): 0x{priv_key:x}\n")
                        f.write(f"Private Key (decimal): {priv_key}\n")
                        f.write(f"Compressed Address: {addr_comp}\n")
                        f.write(f"Uncompressed Address: {addr_uncomp}\n")
                    
                    return
            except queue.Empty:
                continue
            
    except KeyboardInterrupt:
        print("\nSearch interrupted by user")
    finally:
        # Cleanup
        for t in threads:
            t.join(timeout=1)

if __name__ == '__main__':
    # Print system info
    print(f"CPU cores available: {cpu_count()}")
    print(f"Python executable: {os.path.realpath(sys.executable)}")
    print("=" * 50)
    
    main()

