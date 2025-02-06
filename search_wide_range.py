from bitcoin import *
import multiprocessing as mp
from datetime import datetime
import time

def check_range(start_value, count, target_address, result_queue, process_id):
    """Check a range of values for matching address"""
    last_report_time = time.time()
    report_interval = 10  # Report every 10 seconds
    
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
                result_queue.put(('FOUND', hex_val, addr, addr_compressed))
                return
            
            # Report progress periodically
            current_time = time.time()
            if current_time - last_report_time > report_interval:
                result_queue.put(('PROGRESS', process_id, hex_val, addr, addr_compressed))
                last_report_time = current_time
                
        except Exception as e:
            if offset % 1000 == 0:  # Report errors less frequently
                result_queue.put(('ERROR', process_id, str(e), hex_val))
            continue

def search_parallel(base_value, range_per_direction=1_000_000_000_000, processes=8):
    """Search in parallel using multiple processes"""
    target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
    
    # Create a queue for results
    result_queue = mp.Queue()
    
    # Calculate range for each process
    values_per_process = range_per_direction // (processes // 2)
    
    print(f"Starting search with {processes} processes")
    print(f"Base value: 0x{base_value:x}")
    print(f"Range per direction: ±{range_per_direction:,}")
    print(f"Values per process: {values_per_process:,}")
    
    # Start processes
    running_processes = []
    
    # Start processes for positive direction
    for i in range(processes // 2):
        start = base_value + (i * values_per_process)
        p = mp.Process(target=check_range, 
                      args=(start, values_per_process, target_address, result_queue, f"pos_{i}"))
        running_processes.append(p)
        p.start()
    
    # Start processes for negative direction
    for i in range(processes // 2):
        start = base_value - ((i + 1) * values_per_process)
        p = mp.Process(target=check_range, 
                      args=(start, values_per_process, target_address, result_queue, f"neg_{i}"))
        running_processes.append(p)
        p.start()
    
    # Monitor progress
    found = False
    while any(p.is_alive() for p in running_processes):
        try:
            msg_type, *data = result_queue.get(timeout=1)
            
            if msg_type == 'FOUND':
                priv_key, addr_uncomp, addr_comp = data
                print("\nMATCH FOUND!")
                print(f"Private Key: {priv_key}")
                print(f"Uncompressed Address: {addr_uncomp}")
                print(f"Compressed Address: {addr_comp}")
                found = True
                break
            
            elif msg_type == 'PROGRESS':
                proc_id, current_val, addr_uncomp, addr_comp = data
                print(f"\nProcess {proc_id} at: 0x{current_val}")
                print(f"Sample addresses:")
                print(f"  Uncompressed: {addr_uncomp}")
                print(f"  Compressed: {addr_comp}")
            
            elif msg_type == 'ERROR':
                proc_id, error_msg, val = data
                print(f"\nError in process {proc_id} at 0x{val}: {error_msg}")
                
        except mp.queues.Empty:
            continue
        
        if found:
            break
    
    # Cleanup
    for p in running_processes:
        p.terminate()
        p.join()
    
    if not found:
        print("\nNo match found in specified range")

if __name__ == '__main__':
    # Our calculated base value
    base_value = 0x16230cfcfa9
    
    # Search ±1 trillion values by default
    range_size = 1_000_000_000_000
    
    # Use 8 processes by default
    num_processes = 8
    
    print("Starting wide range search...")
    print("=" * 50)
    
    try:
        search_parallel(base_value, range_size, num_processes)
    except KeyboardInterrupt:
        print("\nSearch interrupted by user")
    except Exception as e:
        print(f"\nError: {str(e)}")

