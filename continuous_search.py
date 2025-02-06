from bitcoin import *
from decimal import Decimal, getcontext
import time
from datetime import datetime

# Set precision
getcontext().prec = 1000

class PuzzleSearch:
    def __init__(self):
        self.BASE_VALUE = 0x4a7711aa5  # Puzzle 58 value
        self.TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        self.CURRENT_GUESS = 0x16230cfcf80
        self.keys_checked = 0
        self.start_time = time.time()

    def check_pattern_match(self, value, base_value, target_preserved_bits=50):
        """Check if a value matches relaxed criteria"""
        # Convert to binary
        val_bin = bin(value)[2:].zfill(64)
        base_bin = bin(base_value)[2:].zfill(64)
        
        # Count preserved bits (relaxed)
        preserved = sum(1 for a, b in zip(val_bin, base_bin) if a == b)
        if abs(preserved - target_preserved_bits) > 5:
            return False
        
        # Check modulo pattern (relaxed range)
        mod = value % 0x29
        if mod < 0x15 or mod > 0x28:
            return False
        
        # Check bit length (exact)
        if len(bin(value)[2:]) != 41:
            return False
        
        # Check ratio (relaxed)
        ratio = Decimal(value) / Decimal(base_value)
        expected_ratio = Decimal('76.1034')
        if abs(ratio - expected_ratio) > Decimal('1.0'):
            return False
        
        return True

    def analyze_value(self, value):
        """Detailed analysis of a value"""
        val_bin = bin(value)[2:].zfill(64)
        base_bin = bin(self.BASE_VALUE)[2:].zfill(64)
        
        preserved = sum(1 for a, b in zip(val_bin, base_bin) if a == b)
        mod = value % 0x29
        ratio = Decimal(value) / Decimal(self.BASE_VALUE)
        
        transitions_01 = sum(1 for a, b in zip(base_bin, val_bin) if a == '0' and b == '1')
        transitions_10 = sum(1 for a, b in zip(base_bin, val_bin) if a == '1' and b == '0')
        
        return {
            'preserved_bits': preserved,
            'modulo': hex(mod),
            'ratio': float(ratio),
            '0->1_transitions': transitions_01,
            '1->0_transitions': transitions_10,
            'binary_length': len(bin(value)[2:])
        }

    def verify_address(self, value):
        """Generate and verify addresses for a value"""
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
        elapsed_time = time.time() - self.start_time
        keys_per_second = self.keys_checked / elapsed_time if elapsed_time > 0 else 0
        
        print(f"\rKeys checked: {self.keys_checked:,} | "
              f"Speed: {keys_per_second:.2f} keys/s | "
              f"Pattern matches: {pattern_matches} | "
              f"Current: 0x{current_value:x}", end='')

    def search_range(self, start_offset, end_offset):
        """Search a range of values"""
        pattern_matches = 0
        last_update = time.time()
        update_interval = 1  # Update progress every second
        
        for offset in range(start_offset, end_offset):
            test_value = self.CURRENT_GUESS + offset
            self.keys_checked += 1
            
            # Progress update
            current_time = time.time()
            if current_time - last_update >= update_interval:
                self.print_progress(test_value, pattern_matches)
                last_update = current_time
            
            if self.check_pattern_match(test_value, self.BASE_VALUE):
                pattern_matches += 1
                addr_uncomp, addr_comp = self.verify_address(test_value)
                
                if addr_uncomp == self.TARGET_ADDRESS or addr_comp == self.TARGET_ADDRESS:
                    print(f"\n\nTARGET ADDRESS FOUND!")
                    print(f"{'='*50}")
                    print(f"Private Key: 0x{test_value:x}")
                    print(f"Uncompressed: {addr_uncomp}")
                    print(f"Compressed: {addr_comp}")
                    analysis = self.analyze_value(test_value)
                    print("\nPattern Analysis:")
                    print(f"Preserved bits: {analysis['preserved_bits']}")
                    print(f"Modulo: {analysis['modulo']}")
                    print(f"Ratio: {analysis['ratio']:.4f}")
                    print(f"0->1 transitions: {analysis['0->1_transitions']}")
                    print(f"1->0 transitions: {analysis['1->0_transitions']}")
                    
                    # Save result to file
                    with open('puzzle67_solution.txt', 'w') as f:
                        f.write(f"Found at: {datetime.now()}\n")
                        f.write(f"Private Key: 0x{test_value:x}\n")
                        f.write(f"Uncompressed Address: {addr_uncomp}\n")
                        f.write(f"Compressed Address: {addr_comp}\n")
                        f.write(f"\nAnalysis:\n")
                        for k, v in analysis.items():
                            f.write(f"{k}: {v}\n")
                    
                    return True
                
                # Detailed output for pattern matches
                if pattern_matches % 10 == 0:
                    print(f"\n\nPattern Match #{pattern_matches}:")
                    print(f"{'='*50}")
                    print(f"Value: 0x{test_value:x}")
                    print(f"Addresses:")
                    print(f"  Uncompressed: {addr_uncomp}")
                    print(f"  Compressed: {addr_comp}")
                    analysis = self.analyze_value(test_value)
                    print("\nPattern Analysis:")
                    print(f"Preserved bits: {analysis['preserved_bits']}")
                    print(f"Modulo: {analysis['modulo']}")
                    print(f"Ratio: {analysis['ratio']:.4f}")
                    print(f"0->1 transitions: {analysis['0->1_transitions']}")
                    print(f"1->0 transitions: {analysis['1->0_transitions']}")
        
        return False

    def continuous_search(self, chunk_size=100000):
        """Continuously search in expanding ranges until found"""
        range_multiplier = 1
        while True:
            print(f"\n\nSearching range {range_multiplier} (±{chunk_size * range_multiplier:,} from base)")
            print(f"{'='*70}")
            
            # Search positive range
            if self.search_range(chunk_size * (range_multiplier-1), chunk_size * range_multiplier):
                return
            
            # Search negative range
            if self.search_range(-chunk_size * range_multiplier, -chunk_size * (range_multiplier-1)):
                return
            
            range_multiplier += 1

if __name__ == '__main__':
    print("Starting continuous search for puzzle 67...")
    print(f"Target address: 1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9")
    print(f"{'='*70}")
    
    searcher = PuzzleSearch()
    searcher.continuous_search()

