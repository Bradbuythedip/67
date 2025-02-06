# Our calculated solution
calc_hex = "16230d4937b"
calc_decimal = int(calc_hex, 16)

# Target puzzle info
target_hex = "0x16230d4937b"

# Known sequence examples
examples = [
    (52, "0xefae164cb9e3c", "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim"),
    (53, "0x180788e47e326c", "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT"),
    (54, "0x236fb6d5ad1f43", "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy"),
    (55, "0x6abe1f9b67e114", "1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa"),
    (56, "0x9d18b63ac4ffdf", "17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi"),
    (57, "0x1eb25c90795d61c", "15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz"),
    (58, "0x2c675b852189a21", "1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf"),
    (59, "0x7496cbb87cab44f", "1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt"),
    (60, "0xfc07a1825367bbe", "1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su")
]

print("Analyzing value patterns:")
print("=" * 50)

print("\nOur calculated solution:")
print(f"Hex: {calc_hex}")
print(f"Decimal: {calc_decimal}")

print("\nKnown examples pattern analysis:")
for puzzle_num, hex_val, addr in examples:
    dec_val = int(hex_val, 16)
    print(f"\nPuzzle {puzzle_num}:")
    print(f"Hex: {hex_val}")
    print(f"Decimal: {dec_val}")
    # Calculate ratio between consecutive values
    if puzzle_num > 52:
        prev_dec = int(examples[puzzle_num-53][1], 16)
        ratio = dec_val / prev_dec
        print(f"Ratio to previous: {ratio:.4f}")

# Compare our solution with puzzle 67 position
print("\nAnalysis of our solution for puzzle 67:")
print("=" * 50)
# Using puzzle 60 as reference
p60_dec = int(examples[-1][1], 16)
steps = 67 - 60
expected_ratio = 1.618033988749895  # φ (golden ratio)
expected_value = p60_dec * (expected_ratio ** steps)

print(f"Puzzle 60 decimal: {p60_dec}")
print(f"Steps to 67: {steps}")
print(f"Expected value using φ^steps: {expected_value:.2f}")
print(f"Our calculated value: {calc_decimal}")
print(f"Difference: {abs(expected_value - calc_decimal):.2f}")
print(f"Ratio: {calc_decimal/expected_value:.4f}")

