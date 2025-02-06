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
    
    def get_fibonacci_number(self, n):
        """Get the nth Fibonacci number"""
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    def calculate_k_value(self, puzzle_number):
        """Calculate k value for a given puzzle number using Fibonacci-based approach"""
        n = puzzle_number - 51
        fib_n = self.get_fibonacci_number(n + 2)  # Offset by 2 to match pattern
        k = GENESIS_TARGET * fib_n // 0x29
        return k
    
    def generate_private_key(self, k_value, puzzle_number):
        """Generate private key using k value and puzzle number"""
        # Use both k value and puzzle number in generation
        base = k_value * GENESIS_TARGET
        offset = (puzzle_number - 51) * 0x29
        
        # Apply additional transformations based on puzzle number
        if puzzle_number % 2 == 0:
            base = base ^ offset
        else:
            base = base + offset
        
        return base % (2**256)
    
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
                return address == known_addresses[puzzle_number]
            
            # For known solutions, verify against known private key
            if puzzle_number in self.known_solutions:
                return private_key == self.known_solutions[puzzle_number]
            
            return True
            
        except Exception as e:
            print(f"Verification error: {str(e)}")
            return False
    
    def solve_puzzle(self, puzzle_number):
        """Solve a specific puzzle"""
        # Calculate k value
        k = self.calculate_k_value(puzzle_number)
        
        # Generate private key
        private_key = self.generate_private_key(k, puzzle_number)
        
        if self.verify_solution(private_key, puzzle_number):
            print(f"\nSolution for Puzzle {puzzle_number}:")
            print(f"k value: 0x{k:x}")
            print(f"Private Key: 0x{private_key:x}")
            
            # Generate WIF formats
            priv_key = hex(private_key)[2:].zfill(64)
            wif_c = encode_privkey(priv_key, 'wif_compressed')
            wif_u = encode_privkey(priv_key, 'wif')
            
            print(f"WIF (compressed):   {wif_c}")
            print(f"WIF (uncompressed): {wif_u}")
            
            # Generate address
            pub_key = privtopub(priv_key)
            address = pubtoaddr(pub_key)
            print(f"Bitcoin Address:    {address}")
            
            return private_key
        return None
    
    def verify_known_solutions(self):
        """Verify pattern against known solutions"""
        print("Verifying Known Solutions:")
        print("=" * 50)
        
        for puzzle_number, known_key in sorted(self.known_solutions.items()):
            k = self.calculate_k_value(puzzle_number)
            generated_key = self.generate_private_key(k, puzzle_number)
            
            print(f"\nPuzzle {puzzle_number}:")
            print(f"Known:     0x{known_key:x}")
            print(f"Generated: 0x{generated_key:x}")
            print(f"k value:   0x{k:x}")
            print(f"Valid:     {generated_key == known_key}")
            
            if generated_key == known_key:
                fib_n = self.get_fibonacci_number(puzzle_number - 49)
                print(f"Fibonacci({puzzle_number - 49}): {fib_n}")
                ratio = Decimal(k) / Decimal(GENESIS_TARGET)
                print(f"k/target ratio: {float(ratio)}")

# Create solver and test
solver = PuzzleSolver()

# First verify pattern with known solutions
solver.verify_known_solutions()

# Then solve puzzle 67
print("\nSolving Puzzle 67...")
solution = solver.solve_puzzle(67)

