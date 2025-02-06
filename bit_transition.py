def analyze_bit_transitions(hex_val1, hex_val2):
    """Analyze how bits change between two consecutive values"""
    val1 = int(hex_val1, 16)
    val2 = int(hex_val2, 16)
    
    bin1 = bin(val1)[2:].zfill(64)
    bin2 = bin(val2)[2:].zfill(64)
    
    # Count transitions
    same_bits = sum(1 for a, b in zip(bin1, bin2) if a == b)
    different_bits = sum(1 for a, b in zip(bin1, bin2) if a != b)
    
    # Analyze patterns
    zero_to_one = sum(1 for a, b in zip(bin1, bin2) if a == '0' and b == '1')
    one_to_zero = sum(1 for a, b in zip(bin1, bin2) if a == '1' and b == '0')
    
    return {
        'same_bits': same_bits,
        'different_bits': different_bits,
        'zero_to_one': zero_to_one,
        'one_to_zero': one_to_zero,
        'ratio': val2 / val1
    }

# Known values with n%3 == 1
known_values = [
    (52, "522b1c52"),
    (55, "11f96e31f"),
    (58, "4a7711aa5")
]

print("Analyzing bit transitions between mod3==1 puzzles:")
print("=" * 70)

for i in range(len(known_values)-1):
    curr_num, curr_val = known_values[i]
    next_num, next_val = known_values[i+1]
    
    analysis = analyze_bit_transitions(curr_val, next_val)
    
    print(f"\nFrom puzzle {curr_num} to {next_num}:")
    print(f"Values: 0x{curr_val} -> 0x{next_val}")
    print(f"Same bits: {analysis['same_bits']}")
    print(f"Different bits: {analysis['different_bits']}")
    print(f"0->1 transitions: {analysis['zero_to_one']}")
    print(f"1->0 transitions: {analysis['one_to_zero']}")
    print(f"Value ratio: {analysis['ratio']:.4f}")

# Now analyze transition patterns leading to our current guess
base_values = [
    (58, "4a7711aa5"),  # Last known mod3==1
    (67, "16230cfcf80")  # Our current guess
]

print("\nAnalyzing transition to our guess:")
print("=" * 70)

analysis = analyze_bit_transitions(base_values[0][1], base_values[1][1])
print(f"\nFrom puzzle {base_values[0][0]} to {base_values[1][0]}:")
print(f"Values: 0x{base_values[0][1]} -> 0x{base_values[1][1]}")
print(f"Same bits: {analysis['same_bits']}")
print(f"Different bits: {analysis['different_bits']}")
print(f"0->1 transitions: {analysis['zero_to_one']}")
print(f"1->0 transitions: {analysis['one_to_zero']}")
print(f"Value ratio: {analysis['ratio']:.4f}")

# Calculate expected transitions based on pattern
avg_same_bits = 64 - (analysis['different_bits'] // 3)  # Adjust for puzzle distance
expected_transitions = analysis['different_bits'] // 3

print("\nExpected pattern for puzzle 67:")
print("=" * 70)
print(f"Should have ~{avg_same_bits} bits same as puzzle 58")
print(f"Should have ~{expected_transitions} bit transitions")

# Test some values around our guess
print("\nTesting values around our guess:")
print("=" * 70)

base = int("16230cfcf80", 16)
for offset in [-3, -2, -1, 0, 1, 2, 3]:
    test_val = hex(base + offset)[2:]
    analysis = analyze_bit_transitions(base_values[0][1], test_val)
    print(f"\nOffset {offset:+d} (0x{test_val}):")
    print(f"Same bits: {analysis['same_bits']}")
    print(f"Different bits: {analysis['different_bits']}")
    print(f"Matches expected pattern: {abs(analysis['different_bits'] - expected_transitions) <= 2}")

