from bitcoin import *
from decimal import Decimal, getcontext
import time
from datetime import datetime
import sys

# Set precision
getcontext().prec = 1000

class ExactMatchSearch:
    def __init__(self):
        self.TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        self.PUZZLE_66 = 0x2832ED74F2B5E35EE
        self.PUZZLE_68 = 0x4F463CE6CD49BF595
        self.keys_checked = 0
        self.start_time = time.time()
        
        print(f"Initializing search for exact address: {self.TARGET_ADDRESS}")
        print("=" * 70)

    def verify_address(self, private_key_int):
        """Generate and verify Bitcoin address"""
        try:
            # Convert to hex and pad
            hex_val = hex(private_key_int)[2:].zfill(64)
            
            # Generate public key
            pub = privtopub(hex_val)
            pub_compressed = compress(pub)
            
            # Generate compressed address only (we know target is compressed)
            addr_compressed = pubtoaddr(pub_compressed)
            
            # Immediately return True if exact match found
            if addr_compressed == self.TARGET_ADDRESS:
                return True, addr_compressed
            
            return False, addr_compressed
            
        except Exception as e:
            return False, str(e)

    def verify_constraints(self, value):
        """Verify if value meets all constraints"""
        try:
            # Check bit length (should be ~66 bits)
            bit_length = len(bin(value)[2:])
            if bit_length != 66:
                return False
                
            # Check modulo pattern
            mod_29 = value % 0x29
            if mod_29 not in [0x1b, 0x1c, 0x1d, 0x1e, 0x1f]:
                return False
                
            # Check ratio to puzzle 66
            ratio_66 = Decimal(value) / Decimal(self.PUZZLE_66)
            if not (Decimal('1.4') < ratio_66 < Decimal('1.6')):
                return False
                
            # Check ratio to puzzle 68
            ratio_68 = Decimal(self.PUZZLE_68) / Decimal(value)
            if not (Decimal('1.4') < ratio_68 < Decimal('1.6')):
                return False
            
            return True
            
        except Exception as e:
            print(f"\nError in constraints check: {str(e)}")
            return False

    def print_progress(self, current_value, pattern_matches, latest_addr=None):
        """Print search progress"""
        elapsed = time.time() - self.start_time
        speed = self.keys_checked / elapsed if elapsed > 0 else 0
        
        sys.stdout.write("\033[K")  # Clear line
        print(f"\rKeys: {self.keys_checked:,} | "
              f"Speed: {speed:.2f} k/s | "
              f"Matches: {pattern_matches} | "
              f"Current: 0x{current_value:x}", end='')
        if latest_addr:
            print(f"\nLatest compressed addr: {latest_addr}", end='')
        sys.stdout.flush()

    def save_solution(self, private_key, address):
        """Save found solution to file"""
        with open('puzzle67_solution.txt', 'w') as f:
            f.write(f"Found at: {datetime.now()}\n")
            f.write(f"Private Key: 0x{private_key:x}\n")
            f.write(f"Address: {address}\n")
            f.write(f"Target: {self.TARGET_ADDRESS}\n")
            f.write(f"\nVerification:\n")
            f.write(f"Ratio to 66: {float(Decimal(private_key) / Decimal(self.PUZZLE_66)):.10f}\n")
            f.write(f"Ratio to 68: {float(Decimal(self.PUZZLE_68) / Decimal(private_key)):.10f}\n")
            f.write(f"Modulo 0x29: 0x{private_key % 0x29:x}\n")
            f.write(f"Bit length: {len(bin(private_key)[2:])}\n")

    def search_range(self, start_value, range_size):
        """Search a specific range of values"""
        pattern_matches = 0
        last_update = time.time()
        latest_addr = None
        
        for offset in range(range_size):
            test_value = start_value + offset
            self.keys_checked += 1
            
            # Update progress
            if time.time() - last_update >= 0.5:  # Update every 0.5 seconds
                self.print_progress(test_value, pattern_matches, latest_addr)
                last_update = time.time()
            
            # First check basic constraints (faster)
            if self.verify_constraints(test_value):
                pattern_matches += 1
                
                # Then verify address (more expensive)
                is_match, address = self.verify_address(test_value)
                latest_addr = address
                
                if is_match:
                    print("\n\nEXACT MATCH FOUND!")
                    print("=" * 50)
                    print(f"Private Key: 0x{test_value:x}")
                    print(f"Address: {address}")
                    print(f"Matches Target: {address == self.TARGET_ADDRESS}")
                    
                    # Save solution
                    self.save_solution(test_value, address)
                    return True
                
                # Show details for pattern matches
                if pattern_matches % 10 == 0:
                    print(f"\n\nPattern Match #{pattern_matches}:")
                    print(f"Value: 0x{test_value:x}")
                    print(f"Address: {address}")
                    print(f"Target: {self.TARGET_ADDRESS}")
        
        return False

    def run_search(self):
        """Run search with expanding ranges"""
        # Calculate expected value
        expected = int(Decimal(self.PUZZLE_66) * (Decimal(self.PUZZLE_68) / Decimal(self.PUZZLE_66)).sqrt())
        
        print(f"Starting search from expected value: 0x{expected:x}")
        print("=" * 70)
        
        range_size = 1000000
        multiplier = 1
        
        while True:
            print(f"\n\nSearching range {multiplier} (±{range_size * multiplier:,})")
            print("-" * 50)
            
            # Search positive direction
            if self.search_range(expected, range_size * multiplier):
                return
            
            # Search negative direction
            if self.search_range(expected - range_size * multiplier, range_size * multiplier):
                return
            
            multiplier += 1

if __name__ == '__main__':
    try:
        searcher = ExactMatchSearch()
        searcher.run_search()
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user")
    except Exception as e:
        print(f"\n\nError: {str(e)}")
