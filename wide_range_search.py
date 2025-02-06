from bitcoin import *
import multiprocessing as mp
from datetime import datetime

def check_range(start_value, count, target_address, result_queue):
    """Check a range of values for matching address"""
    for offset in range(count):
        test_value = start_value + offset
        hex_val = hex(test_value)[2:].zfill(64)
        
        try:
            # Check both compressed and uncompressed
            pub = privtopub(hex_val)
            pub_compressed = compress(pub)
            
            addr = pubtoaddr(pub)
            addr_compressed = pubtoaddr(pub_compressed)
            
            # Check if either matches
            if addr == target_address or addr_compressed == target_address:
                result_queue.put((hex_val, addr, addr_compressed))
                return
            
            # Print progress every 1000 values
            if offset % 1000 == 0:
                print(f"Checked up to: 0x{hex_val} ({datetime.now()})")
                print(f"Sample addresses - Uncompressed: {addr}, Compressed: {addr_compressed}")
                
        except Exception as e:
            continue

def parallel_search(base_value, range_size, num_processes):
    """Search in parallel using multiple processes"""
    target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
    
    # Create a queue for results
    result_queue = mp.Queue()
    
    # Split the range into chunks for each process
    chunk_size = range_size // num_processes
    processes = []
    
    print(f"Starting search with {num_processes} processes")
    print(f"Base value: 0x{base_value:x}")
    print(f"Range size: {range_size}")
    print(f"Chunk size: {chunk_size}")
    
    # Start processes for positive offsets
    for i in range(num_processes // 2):
        start = base_value + (i * chunk_size)
        p = mp.Process(target=check_range, args=(start, chunk_size, target_address, result_queue))
        processes.append(p)
        p.start()
    
    # Start processes for negative offsets
    for i in range(num_processes // 2):
        start = base_value - ((i + 1) * chunk_size)
        p = mp.Process(target=check_range, args=(start, chunk_size, target_address, result_queue))
        processes.append(p)
        p.start()
    
    # Wait for a result or for all processes to complete
    result = None
    while any(p.is_alive() for p in processes):
        try:
            result = result_queue.get(timeout=1)
            break
        except:
            continue
    
    # Terminate all processes
    for p in processes:
        p.terminate()
    
    return result

if __name__ == '__main__':
    # Base value from our previous calculation
    base_value = 0x16230cfcfa9
    
    # Search a much wider range (±1 trillion)
    range_size = 1_000_000_000_000
    
    # Use 8 processes for parallel search
    num_processes = 8
    
    print("Starting wide range search...")
    print("=" * 50)
    
    result = parallel_search(base_value, range_size, num_processes)
    
    if result:
        priv_key, addr_uncomp, addr_comp = result
        print("\nMATCH FOUND!")
        print(f"Private Key: {priv_key}")
        print(f"Uncompressed Address: {addr_uncomp}")
        print(f"Compressed Address: {addr_comp}")
    else:
        print("\nNo match found in specified range")

