from bitcoin import *
import math
from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
GENESIS_TARGET = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

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
        
    def calculate_k_value(self, puzzle_number):
        """Calculate k value for a given puzzle number"""
        power = puzzle_number - 51  # Adjust for puzzle numbering
        phi_power = pow(PHI, Decimal(power))
        k = int(GENESIS_TARGET * phi_power)
        return k
    
    def verify_solution(self, puzzle_number, private_key):
        """Verify if a private key is valid for a puzzle"""
        try:
            # Convert private key to proper format
            priv_key = hex(private_key)[2:].zfill(64)
            
            # Generate public key and address
            pub_key = privtopub(priv_key)
            address = pubtoaddr(pub_key)
            
            # Known addresses for verification
            known_addresses = {
                67: "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
                68: "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
                69: "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG"
            }
            
            if puzzle_number in known_addresses:
                return address == known_addresses[puzzle_number]
            
            return True  # For other numbers, we just check if key is valid
            
        except Exception as e:
            print(f"Verification error: {str(e)}")
            return False
    
    def generate_solution(self, puzzle_number):
        """Generate solution for a specific puzzle number"""
        # Calculate k value
        k = self.calculate_k_value(puzzle_number)
        
        # If it's a known solution, verify our k calculation
        if puzzle_number in self.known_solutions:
            known_key = self.known_solutions[puzzle_number]
            print(f"\nPuzzle {puzzle_number}:")
            print(f"Known solution:  0x{known_key:x}")
            print(f"Calculated k:    0x{k:x}")
            print(f"φ^{puzzle_number-51} ≈ {int(pow(PHI, puzzle_number-51))}")
            
        # Generate private key using k value
        private_key = k * GENESIS_TARGET % (2**256)
        
        # Verify solution
        if self.verify_solution(puzzle_number, private_key):
            return private_key
        return None
    
    def analyze_pattern(self, start_num=52, end_num=70):
        """Analyze pattern across a range of puzzle numbers"""
        print("\nAnalyzing Pattern:")
        print("=" * 50)
        
        previous_k = None
        for num in range(start_num, end_num + 1):
            k = self.calculate_k_value(num)
            
            print(f"\nPuzzle {num}:")
            print(f"k value: 0x{k:x}")
            print(f"φ^{num-51} ≈ {int(pow(PHI, num-51))}")
            
            if previous_k:
                ratio = Decimal(k) / Decimal(previous_k)
                print(f"Ratio to previous: {float(ratio)}")
                print(f"Difference from φ: {abs(float(ratio - PHI))}")
            
            if num in self.known_solutions:
                print(f"Known solution: 0x{self.known_solutions[num]:x}")
                solution = self.generate_solution(num)
                print(f"Generated:      0x{solution:x}")
                print(f"Match: {'✓' if solution == self.known_solutions[num] else '✗'}")
            
            previous_k = k
    
    def solve_puzzle(self, puzzle_number):
        """Solve a specific puzzle number"""
        solution = self.generate_solution(puzzle_number)
        
        if solution:
            print(f"\nSolution for Puzzle {puzzle_number}:")
            print(f"Private Key: 0x{solution:x}")
            
            # Generate WIF formats
            priv_key = hex(solution)[2:].zfill(64)
            wif_c = encode_privkey(priv_key, 'wif_compressed')
            wif_u = encode_privkey(priv_key, 'wif')
            
            print(f"WIF (compressed):   {wif_c}")
            print(f"WIF (uncompressed): {wif_u}")
            
            # Generate address
            pub_key = privtopub(priv_key)
            address = pubtoaddr(pub_key)
            print(f"Bitcoin Address:    {address}")
            
            return solution
        return None

# Create solver and test
solver = PuzzleSolver()

# First verify pattern with known solutions
print("Verifying Pattern with Known Solutions")
solver.analyze_pattern(52, 60)

# Then solve target puzzle
print("\nSolving Puzzle 67")
solution_67 = solver.solve_puzzle(67)

if solution_67:
    # Verify solution matches target address
    priv_key = hex(solution_67)[2:].zfill(64)
    pub_key = privtopub(priv_key)
    address = pubtoaddr(pub_key)
    print(f"\nVerification:")
    print(f"Generated Address: {address}")
    print(f"Target Address:    1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9")
    print(f"Match: {'✓' if address == '1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9' else '✗'}")

