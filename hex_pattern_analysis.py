from decimal import Decimal, getcontext
getcontext().prec = 100

# Known hex values from privkeys
hex_values = [
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

def analyze_patterns():
    print("Analyzing Hex Value Patterns:")
    print("=" * 50)
    
    for i, (puzzle, value) in enumerate(hex_values):
        print(f"\nPuzzle {puzzle}:")
        print(f"Hex value: 0x{value:x}")
        
        # For consecutive values
        if i > 0:
            prev_puzzle, prev_value = hex_values[i-1]
            ratio = value / prev_value
            print(f"Ratio to previous: {ratio:.4f}")
        
        # Analyze byte patterns
        bytes_arr = [(value >> i) & 0xFF for i in range(0, 64, 8)]
        print("Byte pattern:", ' '.join([f"{b:02x}" for b in bytes_arr if b != 0]))
        
        # Check divisibility by key numbers
        for div in [0x29, 0x15, 0x8e]:
            if value % div == 0:
                print(f"Divisible by 0x{div:x}")
        
        # Look for recurring patterns
        hex_str = f"{value:x}"
        for length in range(2, min(len(hex_str), 5)):
            for start in range(len(hex_str) - length + 1):
                pattern = hex_str[start:start+length]
                if hex_str.count(pattern) > 1:
                    print(f"Recurring pattern: {pattern}")

def find_phi_relationship():
    """Analyze relationship with golden ratio"""
    phi = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
    
    print("\nGolden Ratio Analysis:")
    print("=" * 50)
    
    for i, (puzzle, value) in enumerate(hex_values):
        n = puzzle - 51  # Offset from puzzle 51
        phi_power = pow(phi, n)
        
        print(f"\nPuzzle {puzzle} (φ^{n}):")
        print(f"Value:     0x{value:x}")
        print(f"φ^{n} ≈ {float(phi_power):.4f}")
        
        # Check if value is related to phi power
        ratio = Decimal(value) / phi_power
        print(f"Value/φ^n: {float(ratio):.4f}")
        
        # Try to find multiplier pattern
        multiplier = value / (2**n)
        print(f"Value/2^n: {float(multiplier):.4f}")

def predict_next_values():
    """Try to predict values for puzzles 67-69"""
    print("\nPredicting Values:")
    print("=" * 50)
    
    # Analyze growth pattern
    growths = []
    for i in range(1, len(hex_values)):
        prev_puzzle, prev_value = hex_values[i-1]
        curr_puzzle, curr_value = hex_values[i]
        growth = curr_value / prev_value
        growths.append(growth)
    
    avg_growth = sum(growths) / len(growths)
    print(f"Average growth factor: {avg_growth:.4f}")
    
    # Last known value
    last_puzzle, last_value = hex_values[-1]
    
    # Predict next values
    for puzzle in range(67, 70):
        steps = puzzle - last_puzzle
        predicted = int(last_value * (avg_growth ** steps))
        print(f"\nPredicted value for puzzle {puzzle}:")
        print(f"0x{predicted:x}")
        
        # Show relationship to known patterns
        print(f"Relationship to 0x29: 0x{predicted % 0x29:x}")
        print(f"Binary length: {len(bin(predicted))-2} bits")

# Run analysis
analyze_patterns()
find_phi_relationship()
predict_next_values()

