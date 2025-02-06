from decimal import Decimal, getcontext
getcontext().prec = 100

# Known pattern progression
known_values = [
    (52, "efae164cb9e3c"),
    (53, "180788e47e326c"),
    (54, "236fb6d5ad1f43"),
    (55, "6abe1f9b67e114"),
    (56, "9d18b63ac4ffdf"),
    (57, "1eb25c90795d61c"),
    (58, "2c675b852189a21"),
    (59, "7496cbb87cab44f"),
    (60, "fc07a1825367bbe")
]

def analyze_hex_digits():
    """Analyze patterns in hex digits"""
    print("Analyzing Hex Digit Patterns:")
    print("=" * 50)
    
    # Look at digit positions and common values
    digit_positions = {}
    for puzzle, value in known_values:
        print(f"\nPuzzle {puzzle}: {value}")
        for pos, digit in enumerate(value):
            if pos not in digit_positions:
                digit_positions[pos] = []
            digit_positions[pos].append(digit)
    
    print("\nDigit position analysis:")
    for pos in sorted(digit_positions.keys()):
        digits = digit_positions[pos]
        print(f"Position {pos}: {digits}")
        # Show most common digits in this position
        common = sorted(set(digits), key=lambda x: digits.count(x), reverse=True)
        print(f"  Most common: {common[:3]}")

def generate_possibilities():
    """Generate possible values for puzzle 67"""
    print("\nGenerating Possibilities for Puzzle 67:")
    print("=" * 50)
    
    # Base possibilities from last few values
    last_values = known_values[-3:]  # Last 3 known values
    
    # Analyze growth pattern
    growths = []
    for i in range(len(known_values)-1):
        curr_val = int(known_values[i][1], 16)
        next_val = int(known_values[i+1][1], 16)
        growth = next_val / curr_val
        growths.append(growth)
        print(f"Growth {known_values[i][0]}->{known_values[i+1][0]}: {growth:.4f}")
    
    avg_growth = sum(growths) / len(growths)
    print(f"\nAverage growth factor: {avg_growth:.4f}")
    
    # Generate base value
    last_val = int(known_values[-1][1], 16)
    steps = 67 - 60  # Steps from puzzle 60 to 67
    
    # Generate variations
    variations = []
    
    # Base prediction
    base_pred = int(last_val * (avg_growth ** steps))
    variations.append(base_pred)
    
    # Variations around the base prediction
    for factor in [0.9, 0.95, 1.05, 1.1]:
        variations.append(int(base_pred * factor))
    
    # Add variations based on digit patterns
    base_hex = hex(base_pred)[2:]
    print(f"\nBase prediction: {base_hex}")
    
    # Generate variations by modifying key digits
    key_digits = ['0', '1', '2', '3', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'e', 'f']
    for pos in range(min(4, len(base_hex))):
        for digit in key_digits:
            new_hex = list(base_hex)
            if pos < len(new_hex):
                new_hex[pos] = digit
                variations.append(int(''.join(new_hex), 16))
    
    # Sort and display unique variations
    unique_vars = sorted(set(variations))
    print("\nPossible values for puzzle 67:")
    for i, var in enumerate(unique_vars[:20]):  # Show top 20 possibilities
        hex_var = hex(var)[2:]
        print(f"Possibility {i+1}: {hex_var}")
        # Show key characteristics
        digit_sum = sum(int(d, 16) for d in hex_var if d.isalnum())
        length = len(hex_var)
        print(f"  Length: {length} digits")
        print(f"  Hex digit sum: {digit_sum}")
        print(f"  First digits: {hex_var[:2]}")
        print(f"  Last digits: {hex_var[-2:]}")

# Run analysis
analyze_hex_digits()
generate_possibilities()

