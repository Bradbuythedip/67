from bitcoin import *
from decimal import Decimal, getcontext
import time
from datetime import datetime

class ProgressiveSearch:
    def __init__(self):
        self.TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        self.PUZZLE_66 = 0x2832ED74F2B5E35EE
        self.PUZZLE_68 = 0x4F463CE6CD49BF595
        
        # Constants from higher puzzle analysis
        self.POWER_BASE = 2  # Base for power progression
        self.keys_checked = 0
        self.start_time = time.time()
        
    def calculate_progression_value(self, puzzle_number, base_value):
        """Calculate value based on power progression"""
        diff = puzzle_number - 66  # Use puzzle 66 as base
        multiplier = self.POWER_BASE ** diff
        return base_value * multiplier
    
    def verify_address(self, value):
        """Generate and verify Bitcoin address"""
        try:
            hex_val = hex(value)[2:].zfill(64)
            pub = privtopub(hex_val)
            pub_compressed = compress(pub)
            addr_compressed = pubtoaddr(pub_compressed)
            
            return addr_compressed == self.TARGET_ADDRESS, addr_compressed
        except:
            return False, None

    def print_progress(self, base_value, power, matches):
        """Print search progress"""
        elapsed = time.time() - self.start_time
        speed = self.keys_checked / elapsed if elapsed > 0 else 0
        
        print(f"\rChecked: {self.keys_checked:,} | "
              f"Speed: {speed:.2f} k/s | "
              f"Matches: {matches} | "
              f"Base: 0x{base_value:x} | "
              f"Power: {power}", end='')

    def search_progression(self, range_size=1000):
        """Search using power progression pattern"""
        print("Starting progressive power-based search...")
        print(f"Target: {self.TARGET_ADDRESS}")
        print("=" * 70)
        
        pattern_matches = 0
        base_value = self.PUZZLE_66
        
        # Search through different base values and powers
        for power in range(-range_size, range_size + 1):
            test_value = self.calculate_progression_value(67, base_value + power)
            self.keys_checked += 1
            
            if self.keys_checked % 1000 == 0:
                self.print_progress(base_value + power, power, pattern_matches)
            
            # Check compressed address
            is_match, address = self.verify_address(test_value)
            
            if is_match:
                print(f"\n\nFOUND TARGET ADDRESS!")
                print("=" * 50)
                print(f"Private Key: 0x{test_value:x}")
                print(f"Address: {address}")
                print(f"Base Value: 0x{base_value + power:x}")
                print(f"Power: {power}")
                
                # Save solution
                with open('puzzle67_solution.txt', 'w') as f:
                    f.write(f"Found: {datetime.now()}\n")
                    f.write(f"Private Key: 0x{test_value:x}\n")
                    f.write(f"Address: {address}\n")
                    f.write(f"Base Value: 0x{base_value + power:x}\n")
                    f.write(f"Power: {power}\n")
                
                return True
            
            # Show pattern matches
            elif address and self.keys_checked % 10000 == 0:
                pattern_matches += 1
                print(f"\n\nPattern Match #{pattern_matches}:")
                print(f"Value: 0x{test_value:x}")
                print(f"Address: {address}")
                print(f"Base: 0x{base_value + power:x}")
                print(f"Power: {power}")
        
        return False

    def run_search(self):
        """Run search with expanding ranges"""
        range_size = 1000
        multiplier = 1
        
        while True:
            print(f"\n\nSearching range {multiplier} (±{range_size * multiplier:,})")
            if self.search_progression(range_size * multiplier):
                return
            multiplier += 1

if __name__ == '__main__':
    try:
        searcher = ProgressiveSearch()
        searcher.run_search()
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user")
    except Exception as e:
        print(f"\n\nError: {str(e)}")

