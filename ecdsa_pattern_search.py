from bitcoin import *
import hashlib
from decimal import Decimal, getcontext
import time
from datetime import datetime

class ECDSAPatternSearch:
    def __init__(self):
        # Known boundaries
        self.PUZZLE_66 = 0x2832ED74F2B5E35EE
        self.PUZZLE_68 = 0x4F463CE6CD49BF595
        self.TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        
        # ECDSA parameters (secp256k1)
        self.N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        self.keys_checked = 0
        self.start_time = time.time()

    def verify_ecdsa_pattern(self, value):
        """Check if value follows ECDSA-like patterns"""
        try:
            # Similar to Genesis block pattern checking
            # k*s ≡ e + rx (mod N)
            k = value % self.N
            
            # Quick modulo checks similar to Genesis pattern
            if k % 0x29 not in [0x1d, 0x1e, 0x1f, 0x20, 0x21]:  # Common modulo values
                return False
                
            # Check high bit patterns (similar to Genesis key)
            high_bits = (k >> 248) & 0xFF
            if high_bits not in [0x16, 0x17, 0x18]:  # Common high byte values
                return False
            
            return True
        except:
            return False

    def verify_address(self, value):
        """Generate and verify address"""
        try:
            hex_val = hex(value)[2:].zfill(64)
            pub = privtopub(hex_val)
            pub_compressed = compress(pub)
            addr = pubtoaddr(pub_compressed)
            
            return addr
        except:
            return None

    def print_progress(self, current, matches):
        """Print search progress"""
        elapsed = time.time() - self.start_time
        speed = self.keys_checked / elapsed if elapsed > 0 else 0
        
        print(f"\rKeys: {self.keys_checked:,} | "
              f"Speed: {speed:.2f} k/s | "
              f"Matches: {matches} | "
              f"Current: 0x{current:x}", end='')

    def search_range(self, start_value, range_size):
        """Search a range of values"""
        matches = 0
        last_update = time.time()
        
        for offset in range(range_size):
            test_value = start_value + offset
            self.keys_checked += 1
            
            # Progress update
            if time.time() - last_update >= 1:
                self.print_progress(test_value, matches)
                last_update = time.time()
            
            # First check ECDSA patterns (faster)
            if self.verify_ecdsa_pattern(test_value):
                # Then verify address (more expensive)
                addr = self.verify_address(test_value)
                
                if addr == self.TARGET_ADDRESS:
                    print(f"\n\nFOUND TARGET!")
                    print("=" * 50)
                    print(f"Private Key: 0x{test_value:x}")
                    print(f"Address: {addr}")
                    
                    # Save solution
                    with open('puzzle67_solution.txt', 'w') as f:
                        f.write(f"Found: {datetime.now()}\n")
                        f.write(f"Private Key: 0x{test_value:x}\n")
                        f.write(f"Address: {addr}\n")
                        # Add ECDSA pattern verification
                        f.write("\nECDSA Pattern Verification:\n")
                        f.write(f"k mod N: 0x{(test_value % self.N):x}\n")
                        f.write(f"High bytes: 0x{(test_value >> 248) & 0xFF:02x}\n")
                        f.write(f"Modulo 0x29: 0x{test_value % 0x29:x}\n")
                    
                    return True
                
                # Show pattern matches
                elif addr and self.keys_checked % 10000 == 0:
                    matches += 1
                    print(f"\nPattern match #{matches}:")
                    print(f"Value: 0x{test_value:x}")
                    print(f"Address: {addr}")
        
        return False

    def run_search(self, chunk_size=1000000):
        """Run search with ECDSA pattern checking"""
        print(f"Starting ECDSA pattern-based search")
        print(f"Target: {self.TARGET_ADDRESS}")
        print("=" * 70)
        
        value_range = self.PUZZLE_68 - self.PUZZLE_66
        chunks = value_range // chunk_size + 1
        
        print(f"Total range: {value_range:,}")
        print(f"Using ECDSA pattern filtering")
        
        for chunk in range(chunks):
            start = self.PUZZLE_66 + (chunk * chunk_size)
            
            print(f"\n\nSearching chunk {chunk + 1}/{chunks}")
            print(f"Starting at: 0x{start:x}")
            
            if self.search_range(start, chunk_size):
                return True
        
        return False

if __name__ == '__main__':
    try:
        searcher = ECDSAPatternSearch()
        searcher.run_search()
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user")
    except Exception as e:
        print(f"\n\nError: {str(e)}")

