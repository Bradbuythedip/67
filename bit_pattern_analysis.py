def analyze_hex_value(value_hex, puzzle_num):
    """Analyze bit patterns and relationships in a hex value"""
    value = int(value_hex, 16)
    binary = bin(value)[2:]
    
    # Basic structure
    structure = {
        'hex_length': len(value_hex),
        'binary_length': len(binary),
        'ones': binary.count('1'),
        'zeros': binary.count('0'),
        'leading_zeros': len(binary) - len(binary.lstrip('0')),
        'trailing_zeros': len(binary) - len(binary.rstrip('0'))
    }
    
    # BASE relationships
    BASE = 0x29
    base_div = value // BASE
    base_mod = value % BASE
    
    # Byte analysis
    bytes_list = [value_hex[i:i+2] for i in range(0, len(value_hex), 2)]
    byte_patterns = {
        'first_byte': bytes_list[0] if bytes_list else None,
        'last_byte': bytes_list[-1] if bytes_list else None,
        'unique_bytes': len(set(bytes_list))
    }
    
    print(f"\nAnalysis for 0x{value_hex} (Puzzle {puzzle_num}):")
    print("=" * 50)
    print(f"Structure:")
    print(f"Hex length: {structure['hex_length']}")
    print(f"Binary length: {structure['binary_length']}")
    print(f"1s/0s ratio: {structure['ones']}/{structure['zeros']}")
    
    print(f"\nBASE (0x29) Relationships:")
    print(f"Division: 0x{base_div:x}")
    print(f"Modulo: 0x{base_mod:x}")
    
    print(f"\nByte Analysis:")
    print(f"First byte: {byte_patterns['first_byte']}")
    print(f"Last byte: {byte_patterns['last_byte']}")
    print(f"Unique bytes: {byte_patterns['unique_bytes']}")
    
    print(f"\nPattern Checks:")
    print(f"Puzzle mod 3: {puzzle_num % 3}")
    if puzzle_num % 3 == 0:
        print(f"XOR with BASE: 0x{(value ^ BASE):x}")
    elif puzzle_num % 3 == 1:
        print(f"OR with BASE: 0x{(value | BASE):x}")
    
    return structure, base_mod

# Known correct values
KNOWN_VALUES = [
    (52, "522b1c52"),
    (53, "7b40aa7b"),
    (54, "a45638a4"),
    (55, "11f96e31f"),
    (56, "1c3ed1bc3"),
    (57, "2e383fee2"),
    (58, "4a7711aa5"),
    (59, "78af51987"),
    (60, "c3266342c")
]

# Analyze known values
print("Analyzing known values:")
for puzzle_num, hex_val in KNOWN_VALUES:
    analyze_hex_value(hex_val, puzzle_num)

# Current candidates
candidates = [
    "16230cfcf80",
    "16230cfcf83",
    "16230cfcf84",
    "16230cfcf85"
]

print("\nAnalyzing candidate values for puzzle 67:")
for candidate in candidates:
    analyze_hex_value(candidate, 67)

