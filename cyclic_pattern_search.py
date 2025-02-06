from bitcoin import *
from decimal import Decimal, getcontext
import time
from datetime import datetime

# Set precision
getcontext().prec = 1000

class CyclicPatternSearch:
    def __init__(self):
        self.PHI = Decimal('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410443207713449470495658467885098743394422125448770664780915884607499887124007652170575179788341662562494075890697040002812104276217711177780531531714101170466659914669798731761356006708748071013179523689427521948435305678300228785699782977834784587822891109762500302696156170025046433824377648610283831268330372429267526311653392473167111211588186385133162038400522216579128667529465490681131715993432359734949850904094762132229810172610705961164562990981629055520852479035240602017279974717534277759277862561943208275051312181562855122248093947123414517022373580577278616008688382952304592647878017889921990270776903895321968198615143780314997411069260886742962267575605231727775203536139362')
        
        # Known puzzles and their modulo values
        self.KNOWN_PUZZLES = [
            (66, 0x2832ED74F2B5E35EE, 0x22),
            (68, 0x4F463CE6CD49BF595, 0x14),
            (69, 0x9E8C79CDB92937B3A, 0x0b),
            (70, 0x349B84B6431A6C4EF1, 0x25)
        ]
        
        self.TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
        self.keys_checked = 0
        self.start_time = time.time()

    def calculate_expected_value(self):
        """Calculate expected value based on known patterns"""
        puzzle_66 = self.KNOWN_PUZZLES[0][1]
        puzzle_68 = self.KNOWN_PUZZLES[1][1]
        
        # Calculate ratio pattern
        ratio_66_68 = Decimal(puzzle_68) / Decimal(puzzle_66)
        expected_ratio_67 = ratio_66_68 ** Decimal('0.5')
        
        return int(Decimal(puzzle_66) * expected_ratio_67)

    def verify_cyclic_pattern(self, value):
        """Verify if value follows the cyclic modulo pattern"""
        mod_29 = value % 0x29
        
        # Expected modulo pattern
        if mod_29 not in [0x1b, 0x1c, 0x1d, 0x1e, 0x1f]:  # Likely values based on pattern
            return False
        
        # Check ratio pattern
        ratio_66 = Decimal(value) / Decimal(self.KNOWN_PUZZLES[0][1])
        ratio_68 = Decimal(self.KNOWN_PUZZLES[1][1]) / Decimal(value)
        
        if not (Decimal('1.4') < ratio_66 < Decimal('1.6')):
            return False
        if not (Decimal('1.4') < ratio_68 < Decimal('1.6')):
            return False
        
        return True

    def verify_address(self, value):
        """Generate and verify Bitcoin address"""
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
        """Search around expected value with cyclic pattern matching"""
        expected = self.calculate_expected_value()
        
        print(f"Starting cyclic pattern search")
        print(f"Expected value around: 0x{expected:x}")
        print("=" * 70)
        
        pattern_matches = 0
        last_update = time.time()
        
        for offset in range(-range_size, range_size + 1):
            test_value = expected + offset
            self.keys_checked += 1
            
            if time.time() - last_update >= 1:
                self.print_progress(test_value, pattern_matches)
                last_update = time.time()
            
            if self.verify_cyclic_pattern(test_value):
                pattern_matches += 1
                addr_uncomp, addr_comp = self.verify_address(test_value)
                
                if addr_comp == self.TARGET_ADDRESS:  # We know it matches compressed format
                    print(f"\n\nSOLUTION FOUND!")
                    print("=" * 50)
                    print(f"Private Key: 0x{test_value:x}")
                    print(f"Compressed Address: {addr_comp}")
                    
                    # Verify patterns
                    ratio_66 = Decimal(test_value) / Decimal(self.KNOWN_PUZZLES[0][1])
                    ratio_68 = Decimal(self.KNOWN_PUZZLES[1][1]) / Decimal(test_value)
                    mod_29 = test_value % 0x29
                    
                    print("\nPattern Verification:")
                    print(f"Ratio to puzzle 66: {float(ratio_66):.10f}")
                    print(f"Ratio to puzzle 68: {float(ratio_68):.10f}")
                    print(f"Modulo 0x29: 0x{mod_29:x}")
                    
                    with open('puzzle67_solution.txt', 'w') as f:
                        f.write(f"Found: {datetime.now()}\n")
                        f.write(f"Private Key: 0x{test_value:x}\n")
                        f.write(f"Compressed Address: {addr_comp}\n")
                        f.write(f"\nVerification:\n")
                        f.write(f"Ratio to 66: {float(ratio_66):.10f}\n")
                        f.write(f"Ratio to 68: {float(ratio_68):.10f}\n")
                        f.write(f"Modulo: 0x{mod_29:x}\n")
                    
                    return True
                
                if pattern_matches % 10 == 0:
                    print(f"\n\nPattern Match #{pattern_matches}:")
                    print(f"Value: 0x{test_value:x}")
                    print(f"Compressed Address: {addr_comp}")
                    print(f"Modulo 0x29: 0x{test_value % 0x29:x}")
        
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
    searcher = CyclicPatternSearch()
    searcher.expand_search()

