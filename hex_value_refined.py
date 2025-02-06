from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
BASE = 0x29

# Known values with pattern confirmations
KNOWN_VALUES = [
    (52, 0x522b1c52, 2),      # φ^1 ≈ 2
    (53, 0x7b40aa7b, 3),      # φ^2 ≈ 3
    (54, 0xa45638a4, 4),      # φ^3 ≈ 4
    (55, 0x11f96e31f, 7),     # φ^4 ≈ 7
    (56, 0x1c3ed1bc3, 11),    # φ^5 ≈ 11
    (57, 0x2e383fee2, 18),    # φ^6 ≈ 18
    (58, 0x4a7711aa5, 29),    # φ^7 ≈ 29
    (59, 0x78af51987, 47),    # φ^8 ≈ 47
    (60, 0xc3266342c, 76)     # φ^9 ≈ 76
]

def analyze_phi_pattern():
    """Analyze exact relationship with phi powers"""
    print("Phi Power Pattern Analysis:")
    print("=" * 50)
    
    for puzzle, value, expected_phi in KNOWN_VALUES:
        n = puzzle - 51  # Power of phi
        phi_power = pow(PHI, n)
        
        print(f"\nPuzzle {puzzle}:")
        print(f"Value:        0x{value:x}")
        print(f"φ^{n} ≈ {float(phi_power):.4f} (expected: {expected_phi})")
        
        # Check pattern with BASE (0x29)
        base_factor = value // BASE
        print(f"Value/0x29:   0x{base_factor:x}")
        
        # Analyze remainder pattern
        remainder = value % BASE
        print(f"Value%0x29:   0x{remainder:x}")
        
        # Compare with expected phi value
        phi_ratio = value / (BASE * expected_phi)
        print(f"Value/(0x29*φ^n): {float(phi_ratio):.4f}")

def predict_value(puzzle_number):
    """Predict value for a given puzzle number using refined pattern"""
    n = puzzle_number - 51
    
    # Calculate phi power approximation
    phi_power = int(round(float(pow(PHI, n))))
    
    # Apply pattern transformation
    value = BASE * phi_power
    
    # Apply puzzle-specific adjustments
    if puzzle_number % 2 == 0:
        value = value ^ BASE
    else:
        value = value | BASE
    
    return value

def verify_pattern():
    """Verify pattern against known values"""
    print("\nPattern Verification:")
    print("=" * 50)
    
    for puzzle, known_value, _ in KNOWN_VALUES:
        predicted = predict_value(puzzle)
        print(f"\nPuzzle {puzzle}:")
        print(f"Known:     0x{known_value:x}")
        print(f"Predicted: 0x{predicted:x}")
        print(f"Match:     {'✓' if predicted == known_value else '✗'}")
        
        if predicted != known_value:
            diff = abs(predicted - known_value)
            print(f"Difference: 0x{diff:x}")

def solve_puzzle_67():
    """Generate solution for puzzle 67"""
    print("\nPuzzle 67 Solution:")
    print("=" * 50)
    
    value = predict_value(67)
    
    print(f"Predicted hex value: 0x{value:x}")
    print(f"Binary length: {len(bin(value))-2} bits")
    print(f"Relationship to 0x29: 0x{value % BASE:x}")
    
    # Show phi power relationship
    n = 67 - 51
    phi_power = int(round(float(pow(PHI, n))))
    print(f"φ^{n} ≈ {phi_power}")
    print(f"Predicted k value: 0x{(value//BASE):x}")

# Run analysis
analyze_phi_pattern()
verify_pattern()
solve_puzzle_67()

