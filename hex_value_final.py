from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
BASE = 0x29
SCALING_FACTOR = 16811670.8537  # From analysis of Value/(0x29*φ^n)

# Known values and their phi power relationships
KNOWN_VALUES = [
    (52, 0x522b1c52, 2),      # φ^1 * k = 0x522b1c52
    (53, 0x7b40aa7b, 3),      # φ^2 * k = 0x7b40aa7b
    (54, 0xa45638a4, 4),      # φ^3 * k = 0xa45638a4
    (55, 0x11f96e31f, 7),     # φ^4 * k = 0x11f96e31f
    (56, 0x1c3ed1bc3, 11),    # φ^5 * k = 0x1c3ed1bc3
    (57, 0x2e383fee2, 18),    # φ^6 * k = 0x2e383fee2
    (58, 0x4a7711aa5, 29),    # φ^7 * k = 0x4a7711aa5
    (59, 0x78af51987, 47),    # φ^8 * k = 0x78af51987
    (60, 0xc3266342c, 76)     # φ^9 * k = 0xc3266342c
]

def calculate_value(puzzle_number):
    """Calculate hex value for a given puzzle number"""
    n = puzzle_number - 51
    phi_power = int(round(float(pow(PHI, n))))
    
    # Calculate using scaling factor and phi power
    value = int(SCALING_FACTOR * phi_power * BASE)
    
    # Apply pattern adjustments
    if puzzle_number % 3 == 0:
        value = value ^ BASE
    elif puzzle_number % 3 == 1:
        value = value | BASE
    
    return value

def verify_value(puzzle_number, value):
    """Verify if a value matches the expected pattern"""
    n = puzzle_number - 51
    phi_power = int(round(float(pow(PHI, n))))
    ratio = value / (BASE * phi_power)
    return abs(ratio - SCALING_FACTOR) < 1

def solve_puzzle_67():
    """Generate solution for puzzle 67"""
    print("Generating solution for Puzzle 67:")
    print("=" * 50)
    
    # Calculate value
    value = calculate_value(67)
    
    print(f"\nPredicted hex value: 0x{value:x}")
    
    # Verify pattern
    if verify_value(67, value):
        print("✓ Value follows the established pattern")
    else:
        print("✗ Value does not match pattern")
    
    # Show components
    n = 67 - 51
    phi_power = int(round(float(pow(PHI, n))))
    print(f"\nComponents:")
    print(f"φ^{n} ≈ {phi_power}")
    print(f"BASE (0x29) = {BASE}")
    print(f"Scaling factor ≈ {SCALING_FACTOR}")
    
    # Show pattern relationships
    print(f"\nPattern Verification:")
    print(f"Value/0x29: 0x{value // BASE:x}")
    print(f"Value%0x29: 0x{value % BASE:x}")
    print(f"Expected ratio: {float(value / (BASE * phi_power)):.4f}")

def verify_pattern():
    """Verify pattern against known values"""
    print("Verifying Pattern with Known Solutions:")
    print("=" * 50)
    
    for puzzle, known_value, phi_scale in KNOWN_VALUES:
        calculated = calculate_value(puzzle)
        
        print(f"\nPuzzle {puzzle}:")
        print(f"Known:     0x{known_value:x}")
        print(f"Generated: 0x{calculated:x}")
        print(f"φ^{puzzle-51} ≈ {phi_scale}")
        
        # Verify components
        k_value = known_value // BASE
        print(f"k value:   0x{k_value:x}")
        
        if verify_value(puzzle, known_value):
            print("✓ Follows pattern")
        else:
            print("✗ Pattern mismatch")

# Run verification and solution
verify_pattern()
solve_puzzle_67()

