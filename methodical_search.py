from bitcoin import *
import time
from datetime import datetime

class MethodicalSearch:
    def __init__(self):
        self.TARGET = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        self.PUZZLE_66 = 0x2832ED74F2B5E35EE
        self.PUZZLE_68 = 0x4F463CE6CD49BF595
        self.keys_checked = 0
        self.start_time = time.time()

    def verify_address(self, value):
        """Generate compressed address for a value"""
        try:
            # Convert to hex and pad
            hex_val = hex(value)[2:].zfill(64)
            
            # Generate public key
            pub = privtopub(hex_val)
            pub_compressed = compress(pub)
            
            # Generate only compressed address
            addr = pubtoaddr(pub_compressed)
            
            return addr
        except Exception as e:
            return None

    def print_progress(self, current, matches):
        """Print search progress"""
        elapsed = time.time() - self.start_time
        speed = self.keys_checked / elapsed if elapsed > 0 else 0
        
        print(f"\rChecked: {self.keys_checked:,} | "
              f"Speed: {speed:.2f} k/s | "
              f"Matches: {matches} | "
              f"Current: 0x{current:x}", end='')

    def search_range(self, start_value, range_size):
        """Search a specific range of values"""
        matches = 0
        last_update = time.time()
        
        for offset in range(range_size):
            test_value = start_value + offset
            self.keys_checked += 1
            
            # Progress update
            if time.time() - last_update >= 1:
                self.print_progress(test_value, matches)
                last_update = time.time()
            
            # Check address
            addr = self.verify_address(test_value)
            if addr == self.TARGET:
                print(f"\n\nFOUND TARGET!")
                print("=" * 50)
                print(f"Private Key: 0x{test_value:x}")
                print(f"Address: {addr}")
                
                # Save result
                with open('puzzle67_solution.txt', 'w') as f:
                    f.write(f"Found: {datetime.now()}\n")
                    f.write(f"Private Key: 0x{test_value:x}\n")
                    f.write(f"Address: {addr}\n")
                return True
            
            # Show occasional matches
            elif addr and self.keys_checked % 10000 == 0:
                matches += 1
                print(f"\nChecked address: {addr}")
        
        return False

    def run_search(self, chunk_size=1000000):
        """Run search in chunks"""
        print(f"Starting methodical search between:")
        print(f"Puzzle 66: 0x{self.PUZZLE_66:x}")
        print(f"Puzzle 68: 0x{self.PUZZLE_68:x}")
        print(f"Target: {self.TARGET}")
        print("=" * 70)
        
        value_range = self.PUZZLE_68 - self.PUZZLE_66
        chunks = value_range // chunk_size + 1
        
        print(f"Total range: {value_range:,}")
        print(f"Chunk size: {chunk_size:,}")
        print(f"Total chunks: {chunks:,}")
        
        for chunk in range(chunks):
            start = self.PUZZLE_66 + (chunk * chunk_size)
            
            print(f"\n\nSearching chunk {chunk + 1}/{chunks}")
            print(f"Starting at: 0x{start:x}")
            
            if self.search_range(start, chunk_size):
                return True
        
        return False

if __name__ == '__main__':
    try:
        searcher = MethodicalSearch()
        searcher.run_search()
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user")
    except Exception as e:
        print(f"\n\nError: {str(e)}")

