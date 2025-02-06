from bitcoin import *
import math
from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
GENESIS_TARGET = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
BASE_PATTERN = 0x29

class PuzzleSolver:
    def __init__(self):
        self.known_solutions = {
            52: 0xefae164cb9e3c,
            53: 0x180788e47e326c,
            54: 0x236fb6d5ad1f43,
            55: 0x6abe1f9b67e114,
            56: 0x9d18b63ac4ffdf,
            57: 0x1eb25c90795d61c,
            58: 0x2c675b852189a21,
            59: 0x7496cbb87cab44f,
            60: 0xfc07a1825367bbe
        }
    
    def calculate_phi_power(self, n):
        """Calculate power of phi and round to nearest integer"""
        phi_power = pow(PHI, Decimal(n))
        return int(round(phi_power))
    
    def calculate_k_value(self, puzzle_number):
        """Calculate k value using phi powers"""
        n = puzzle_number - 51  # Offset from puzzle 51
        phi_power = self.calculate_phi_power(n)
        k = (GENESIS_TARGET * phi_power) >> 8  # Shift to maintain reasonable size
        return k
    
    def generate_private_key(self, puzzle_number):
        """Generate private key for a puzzle"""
        k = self.calculate_k_value(puzzle_number)
        n = puzzle_number - 51
        
        # Calculate base components
        time_component = k * GENESIS_TARGET
        pattern_component = BASE_PATTERN * self.calculate_phi_power(n)
        
        # Combine components
        if puzzle_number % 2 == 0:
            private_key = (time_component + pattern_component) % (2**256)
        else:
            private_key = (time_component ^ pattern_component) % (2**256)
        
        return private_key
    
    def verify_solution(self, private_key, puzzle_number):
        """Verify if a private key is valid for a puzzle"""
        try:
            # Convert to proper format
            priv_key = hex(private_key)[2:].zfill(64)
            
            # Generate public key and address
            pub_key = privtopub(priv_key)
            address = pubtoaddr(pub_key)
            
            # Known addresses
            known_addresses = {
                67: "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
                68: "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
                69: "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG"
            }
            
            if puzzle_number in known_addresses:
                match = address == known_addresses[puzzle_number]
                print(f"Generated address: {address}")
                print(f"Target address:    {known_addresses[puzzle_number]}")
                return match
            
            # For known solutions, verify against known private key
            if puzzle_number in self.known_solutions:
                return private_key == self.known_solutions[puzzle_number]
            
            return True
            
        except Exception as e:
            print(f"Verification error: {str(e)}")
            return False
    
    def analyze_solution(self, puzzle_number, private_key):
        """Analyze components of a solution"""
        k = self.calculate_k_value(puzzle_number)
        n = puzzle_number - 51
        phi_power = self.calculate_phi_power(n)
        
        print(f"\nAnalysis for Puzzle {puzzle_number}:")
        print(f"φ^{n} ≈ {phi_power}")
        print(f"k value: 0x{k:x}")
        print(f"Private key: 0x{private_key:x}")
        
        # Check relationships
        print("\nPattern Relationships:")
        print(f"k mod 0x29: 0x{k % BASE_PATTERN:x}")
        print(f"key mod GENESIS: 0x{private_key % GENESIS_TARGET:x}")
        
        # Generate address
        priv_key = hex(private_key)[2:].zfill(64)
        pub_key = privtopub(priv_key)
        address = pubtoaddr(pub_key)
        
        print(f"\nBitcoin Address: {address}")
        
        # Generate WIF formats
        wif_c = encode_privkey(priv_key, 'wif_compressed')
        wif_u = encode_privkey(priv_key, 'wif')
        
        print(f"WIF (compressed):   {wif_c}")
        print(f"WIF (uncompressed): {wif_u}")
    
    def solve_puzzle(self, puzzle_number):
        """Solve a specific puzzle"""
        private_key = self.generate_private_key(puzzle_number)
        
        if self.verify_solution(private_key, puzzle_number):
            self.analyze_solution(puzzle_number, private_key)
            return private_key
        
        return None
    
    def verify_known_solutions(self):
        """Verify pattern against known solutions"""
        print("Verifying Known Solutions:")
        print("=" * 50)
        
        for puzzle_number in sorted(self.known_solutions.keys()):
            print(f"\nPuzzle {puzzle_number}:")
            private_key = self.generate_private_key(puzzle_number)
            known_key = self.known_solutions[puzzle_number]
            
            print(f"Known:     0x{known_key:x}")
            print(f"Generated: 0x{private_key:x}")
            print(f"Valid:     {private_key == known_key}")
            
            if private_key == known_key:
                k = self.calculate_k_value(puzzle_number)
                n = puzzle_number - 51
                phi_power = self.calculate_phi_power(n)
                print(f"φ^{n} ≈ {phi_power}")
                print(f"k value: 0x{k:x}")

# Create solver and test
solver = PuzzleSolver()

# First verify pattern with known solutions
solver.verify_known_solutions()

# Then solve puzzle 67
print("\nSolving Puzzle 67...")
solution = solver.solve_puzzle(67)

