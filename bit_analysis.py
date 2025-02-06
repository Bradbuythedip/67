def analyze_value(value, puzzle_num):
    """Detailed bit and BASE analysis"""
    BASE = 0x29
    
    # Convert to binary and analyze bits
    bits = bin(value)[2:]
    byte_groups = [bits[i:i+8] for i in range(0, len(bits), 8)]
    
    # Analyze BASE relationship
    div = value // BASE
    mod = value % BASE
    
    # Calculate adjustments
    xor_val = value ^ BASE
    or_val = value | BASE
    
    print(f"Analysis for value: 0x{value:x}")
    print("-" * 50)
    print(f"Binary length: {len(bits)}")
    print(f"Byte groups: {' '.join(byte_groups)}")
    print(f"\nBASE (0x29) relationships:")
    print(f"Division: 0x{div:x}")
    print(f"Modulo: 0x{mod:x}")
    print(f"XOR with BASE: 0x{xor_val:x}")
    print(f"OR with BASE: 0x{or_val:x}")
    print(f"\nPuzzle {puzzle_num} % 3 = {puzzle_num % 3}")
    
    # Pattern analysis
    print("\nPattern Analysis:")
    print(f"Leading zeros: {len(bits) - len(bits.lstrip('0'))}")
    print(f"Trailing zeros: {len(bits) - len(bits.rstrip('0'))}")
    print(f"Total 1s: {bits.count('1')}")
    print(f"Total 0s: {bits.count('0')}")
    
    return {
        'bits': bits,
        'div': div,
        'mod': mod,
        'xor': xor_val,
        'or': or_val
    }

# Known correct values
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

print("Analyzing known solution patterns:")
print("=" * 70)

for puzzle_num, value in KNOWN_VALUES:
    print(f"\nPuzzle {puzzle_num}:")
    analysis = analyze_value(value, puzzle_num)

print("\nAnalyzing our prediction for puzzle 67:")
print("=" * 70)
prediction = 0x16230cfcfa9
analysis = analyze_value(prediction, 67)

