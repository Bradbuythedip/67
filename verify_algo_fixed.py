from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
BASE = Decimal('41')  # 0x29
SCALING_FACTOR = Decimal('16811670.8537')

def calculate_value(puzzle_number):
    """Calculate value for a given puzzle number"""
    n = puzzle_number - 51
    phi_power = pow(PHI, n)
    
    # Calculate base value
    value = int(SCALING_FACTOR * phi_power * BASE)
    
    # Apply pattern adjustments
    if puzzle_number % 3 == 0:
        value = value ^ 0x29
    elif puzzle_number % 3 == 1:
        value = value | 0x29
    
    return value

# Known solutions to verify against
KNOWN_VALUES = [
    (52, 0x522b1c52),
    (53, 0x7b40aa7b),
    (54, 0xa45638a4),
    (55, 0x11f96e31f),
    (56, 0x1c3ed1bc3),
    (57, 0x2e383fee2),
    (58, 0x4a7711aa5),
    (59, 0x78af51987),
    (60, 0xc3266342c)
]

print("Verifying algorithm against known solutions:")
print("=" * 50)

for puzzle_num, known_value in KNOWN_VALUES:
    calculated = calculate_value(puzzle_num)
    
    print(f"\nPuzzle {puzzle_num}:")
    print(f"Known:      0x{known_value:x}")
    print(f"Calculated: 0x{calculated:x}")
    print(f"Match?: {calculated == known_value}")
    
    # Show component values
    n = puzzle_num - 51
    phi_power = pow(PHI, n)
    base_value = SCALING_FACTOR * phi_power * BASE
    
    print(f"φ^{n} ≈ {float(phi_power):.4f}")
    print(f"Raw value: {float(base_value):.4f}")
    
    # Show ratio analysis
    ratio = Decimal(known_value) / (BASE * phi_power)
    print(f"Value/(BASE*φ^n): {float(ratio):.4f}")

print("\nNow calculating for puzzle 67:")
print("=" * 50)

p67_value = calculate_value(67)
print(f"\nPredicted value: 0x{p67_value:x}")
print(f"Decimal: {p67_value}")

n = 67 - 51
phi_power = pow(PHI, n)
print(f"φ^{n} ≈ {float(phi_power):.4f}")
ratio = Decimal(p67_value) / (BASE * phi_power)
print(f"Value/(BASE*φ^n): {float(ratio):.4f}")

