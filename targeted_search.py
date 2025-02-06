from bitcoin import *
from decimal import Decimal, getcontext
import time
from datetime import datetime

# Set precision
getcontext().prec = 1000

class TargetedSearch:
    def __init__(self):
        self.PUZZLE_66 = 0x2832ED74F2B5E35EE
        self.PUZZLE_68 = 0x4F463CE6CD49BF595
        self.TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        self.keys_checked = 0
        self.start_time = time.time()
        
        # Calculate expected value range
        self.ratio_66_68 = Decimal(self.PUZZLE_68) / Decimal(self.PUZZLE_66)
        self.expected_67 = int(self.PUZZLE_66 * (1 + (self.ratio_66_68 - 1) / 2))

    def check_constraints(self, value):
        """Check if value meets the observed constraints"""
        # Check bit length
        bit_length = len(bin(value)[2:])
        if bit_length != 66:
            return False
            
        # Check modulo range
        mod = value % 0x29
        if mod < 0x14 or mod > 0x22:
            return False
            
        # Check ratio with puzzle 66
        ratio = Decimal(value) / Decimal(self.PUZZLE_66)
        if ratio < Decimal('1.4') or ratio > Decimal('1.6'):
            return False
            
        # Check bit transitions
        bin_66 = bin(self.PUZZLE_66)[2:].zfill(256)
        bin_val = bin(value)[2:].zfill(256)
        preserved = sum(1 for a, b in zip(bin_66, bin_val) if a == b)
        if preserved < 215 or preserved > 225:
            return False
            
        return True

    def verify_address(self, value):
        """Generate and verify address"""
        try:
            hex_val = hex(value)[2:].zfill(64)
            pub = privtopub(hex_val)
            pub_compressed = compress(pub)
            
            addr = pubtoaddr(pub)
            addr_compressed = pubtoaddr(pub_compressed)
            
            return addr, addr_compressed
        except:
            return None, None

    def print_progress(self, current_value, pattern_matches):
        """Print search progress"""
        elapsed = time.time() - self.start_time
        speed = self.keys_checked / elapsed if elapsed > 0 else 0
        
        print(f"\rChecked: {self.keys_checked:,} | "
              f"Speed: {speed:.2f} k/s | "
              f"Matches: {pattern_matches} | "
              f"Current: 0x{current_value:x}", end='')

    def search(self, range_size=1000000):
        """Search around expected value"""
        print(f"Starting targeted search based on puzzles 66 and 68")
        print(f"Expected value around: 0x{self.expected_67:x}")
        print("=" * 70)
        
        pattern_matches = 0
        last_update = time.time()
        
        # Search around expected value
        for offset in range(-range_size, range_size + 1):
            test_value = self.expected_67 + offset
            self.keys_checked += 1
            
            # Progress update
            if time.time() - last_update >= 1:
                self.print_progress(test_value, pattern_matches)
                last_update = time.time()
            
            if self.check_constraints(test_value):
                pattern_matches += 1
                addr_uncomp, addr_comp = self.verify_address(test_value)
                
                if addr_uncomp == self.TARGET_ADDRESS or addr_comp == self.TARGET_ADDRESS:
                    print(f"\n\nSOLUTION FOUND!")
                    print("=" * 50)
                    print(f"Private Key: 0x{test_value:x}")
                    print(f"Uncompressed: {addr_uncomp}")
                    print(f"Compressed: {addr_comp}")
                    
                    # Calculate ratios
                    ratio_66 = Decimal(test_value) / Decimal(self.PUZZLE_66)
                    ratio_68 = Decimal(self.PUZZLE_68) / Decimal(test_value)
                    
                    print("\nVerification:")
                    print(f"Ratio to puzzle 66: {float(ratio_66):.10f}")
                    print(f"Ratio to puzzle 68: {float(ratio_68):.10f}")
                    print(f"Modulo 0x29: 0x{test_value % 0x29:x}")
                    print(f"Bit length: {len(bin(test_value)[2:])}")
                    
                    # Save to file
                    with open('puzzle67_solution.txt', 'w') as f:
                        f.write(f"Found: {datetime.now()}\n")
                        f.write(f"Private Key: 0x{test_value:x}\n")
                        f.write(f"Uncompressed: {addr_uncomp}\n")
                        f.write(f"Compressed: {addr_comp}\n")
                        f.write(f"\nVerification:\n")
                        f.write(f"Ratio to 66: {float(ratio_66):.10f}\n")
                        f.write(f"Ratio to 68: {float(ratio_68):.10f}\n")
                        f.write(f"Modulo: 0x{test_value % 0x29:x}\n")
                        f.write(f"Bits: {len(bin(test_value)[2:])}\n")
                    
                    return True
                
                if pattern_matches % 10 == 0:
                    print(f"\n\nPattern Match #{pattern_matches}:")
                    print(f"Value: 0x{test_value:x}")
                    print(f"Addresses:")
                    print(f"  Uncompressed: {addr_uncomp}")
                    print(f"  Compressed: {addr_comp}")
                    ratio = Decimal(test_value) / Decimal(self.PUZZLE_66)
                    print(f"Ratio to puzzle 66: {float(ratio):.10f}")
        
        return False

    def expand_search(self):
        """Continue searching in expanding ranges"""
        range_size = 1000000
        multiplier = 1
        
        while True:
            print(f"\n\nSearching range {multiplier} (±{range_size * multiplier:,})")
            if self.search(range_size * multiplier):
                return
            multiplier += 1

if __name__ == '__main__':
    searcher = TargetedSearch()
    searcher.expand_search()

