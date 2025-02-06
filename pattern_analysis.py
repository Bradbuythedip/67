from decimal import Decimal, getcontext
from datetime import datetime
import hashlib
import base58

# Set very high precision for our calculations
getcontext().prec = 1000

class PuzzleAnalyzer:
    def __init__(self):
        self.PHI = Decimal('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410443207713449470495658467885098743394422125448770664780915884607499887124007652170575179788341662562494075890697040002812104276217711177780531531714101170466659914669798731761356006708748071013179523689427521948435305678300228785699782977834784587822891109762500302696156170025046433824377648610283831268330372429267526311653392473167111211588186385133162038400522216579128667529465490681131715993432359734949850904094762132229810172610705961164562990981629055520852479035240602017279974717534277759277862561943208275051312181562855122248093947123414517022373580577278616008688382952304592647878017889921990270776903895321968198615143780314997411069260886742962267575605231727775203536139362')
        self.BASE = 0x29
        self.SCALING_FACTOR = Decimal('16811670.8537')
        
        # Known solutions for verification
        self.KNOWN_SOLUTIONS = [
            (52, "0x522b1c52", "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim"),
            (53, "0x7b40aa7b", "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT"),
            (54, "0xa45638a4", "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy"),
            (55, "0x11f96e31f", "1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa"),
            (56, "0x1c3ed1bc3", "17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi"),
            (57, "0x2e383fee2", "15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz"),
            (58, "0x4a7711aa5", "1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf"),
            (59, "0x78af51987", "1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt"),
            (60, "0xc3266342c", "1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su")
        ]

    def analyze_value_structure(self, hex_value):
        """Analyze the structure of a hex value"""
        value = int(hex_value, 16)
        binary = bin(value)[2:]
        return {
            'decimal': value,
            'hex_length': len(hex_value[2:]),
            'binary_length': len(binary),
            'binary_ones': binary.count('1'),
            'binary_zeros': binary.count('0'),
            'leading_zeros': len(binary) - len(binary.lstrip('0')),
            'trailing_zeros': len(binary) - len(binary.rstrip('0')),
            'base_division': value // self.BASE,
            'base_modulo': value % self.BASE
        }

    def analyze_phi_relationships(self, puzzle_number, value):
        """Analyze relationships with φ"""
        n = puzzle_number - 51
        phi_power = pow(self.PHI, n)
        ratio = Decimal(value) / (Decimal(self.BASE) * phi_power)
        return {
            'n': n,
            'phi_power': float(phi_power),
            'ratio': float(ratio),
            'diff_from_scaling': float(abs(ratio - self.SCALING_FACTOR))
        }

    def analyze_patterns(self):
        """Analyze patterns in known solutions"""
        print("Analyzing patterns in known solutions:")
        print("=" * 70)
        
        patterns = []
        for puzzle_num, hex_val, addr in self.KNOWN_SOLUTIONS:
            print(f"\nPuzzle {puzzle_num}:")
            structure = self.analyze_value_structure(hex_val)
            phi_rel = self.analyze_phi_relationships(puzzle_num, int(hex_val, 16))
            
            print("Structure Analysis:")
            print(f"Hex length: {structure['hex_length']}")
            print(f"Binary length: {structure['binary_length']}")
            print(f"Binary 1s/0s: {structure['binary_ones']}/{structure['binary_zeros']}")
            print(f"Base division: 0x{structure['base_division']:x}")
            print(f"Base modulo: 0x{structure['base_modulo']:x}")
            
            print("\nPhi Relationships:")
            print(f"n = {phi_rel['n']}")
            print(f"φ^n ≈ {phi_rel['phi_power']:.4f}")
            print(f"ratio: {phi_rel['ratio']:.4f}")
            print(f"diff from scaling: {phi_rel['diff_from_scaling']:.4f}")
            
            patterns.append({
                'puzzle': puzzle_num,
                'structure': structure,
                'phi_rel': phi_rel
            })
        
        return patterns

    def analyze_progression(self, patterns):
        """Analyze progression between puzzles"""
        print("\nAnalyzing progression between puzzles:")
        print("=" * 70)
        
        for i in range(len(patterns)-1):
            curr = patterns[i]
            next_p = patterns[i+1]
            
            value_ratio = next_p['structure']['decimal'] / curr['structure']['decimal']
            bit_growth = next_p['structure']['binary_length'] - curr['structure']['binary_length']
            
            print(f"\nFrom puzzle {curr['puzzle']} to {next_p['puzzle']}:")
            print(f"Value ratio: {value_ratio:.4f}")
            print(f"Bit growth: {bit_growth}")
            print(f"Modulo change: 0x{curr['structure']['base_modulo']:x} -> 0x{next_p['structure']['base_modulo']:x}")

    def project_puzzle_67(self, patterns):
        """Project patterns to puzzle 67"""
        print("\nProjecting patterns to puzzle 67:")
        print("=" * 70)
        
        # Last known value (puzzle 60)
        last_known = patterns[-1]
        steps = 67 - 60
        
        # Project using different methods
        phi_projection = last_known['structure']['decimal'] * float(pow(self.PHI, steps))
        
        # Average growth ratio from last few puzzles
        growth_ratios = []
        for i in range(len(patterns)-1):
            ratio = patterns[i+1]['structure']['decimal'] / patterns[i]['structure']['decimal']
            growth_ratios.append(ratio)
        avg_ratio = sum(growth_ratios[-3:]) / 3  # Use last 3 ratios
        ratio_projection = last_known['structure']['decimal'] * (avg_ratio ** steps)
        
        print(f"\nProjections for puzzle 67:")
        print(f"Using φ: 0x{int(phi_projection):x}")
        print(f"Using avg ratio: 0x{int(ratio_projection):x}")
        
        # Analyze bit length progression
        bit_lengths = [p['structure']['binary_length'] for p in patterns]
        bit_growth_rate = (bit_lengths[-1] - bit_lengths[0]) / (len(bit_lengths) - 1)
        expected_bits = bit_lengths[-1] + (steps * bit_growth_rate)
        
        print(f"\nBit length analysis:")
        print(f"Expected bits: {int(expected_bits)}")
        print(f"Current guess bits: {len(bin(0x16230cfcfa9)[2:])}")

def main():
    analyzer = PuzzleAnalyzer()
    patterns = analyzer.analyze_patterns()
    analyzer.analyze_progression(patterns)
    analyzer.project_puzzle_67(patterns)

if __name__ == '__main__':
    main()
