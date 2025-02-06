import math

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2

def hex_to_decimal(hex_str):
    return int(hex_str, 16)

# Sample of private keys from the list (first few sequential ones)
privkeys = [
    "0000000000000000000000000000000000000000000000000000000000000001",
    "0000000000000000000000000000000000000000000000000000000000000003",
    "0000000000000000000000000000000000000000000000000000000000000007",
    "0000000000000000000000000000000000000000000000000000000000000008",
    "0000000000000000000000000000000000000000000000000000000000000015",
    "0000000000000000000000000000000000000000000000000000000000000031",
    "000000000000000000000000000000000000000000000000000000000000004c",
    "00000000000000000000000000000000000000000000000000000000000000e0",
]

# Convert hex to decimal
decimals = [hex_to_decimal(key) for key in privkeys]

print("Analysis of first 8 private keys:")
print("\nDecimal values:")
for i, d in enumerate(decimals, 1):
    print(f"Key {i}: {d}")

print("\nRatios between consecutive values:")
for i in range(len(decimals)-1):
    ratio = decimals[i+1] / decimals[i] if decimals[i] != 0 else 0
    print(f"Ratio {i+1}/{i+2}: {ratio}")
    print(f"Difference from PHI: {abs(ratio - PHI)}")

# Check if values follow Fibonacci-like sequence
print("\nChecking for Fibonacci-like properties:")
for i in range(len(decimals)-2):
    sum_check = decimals[i] + decimals[i+1]
    actual_next = decimals[i+2]
    print(f"Sum of {decimals[i]} + {decimals[i+1]} = {sum_check}")
    print(f"Next value is: {actual_next}")
    print(f"Difference: {abs(sum_check - actual_next)}")

# Look for pattern in hex digits
print("\nHex digit patterns:")
for i, key in enumerate(privkeys, 1):
    print(f"Key {i}: {key}")
    # Group by pairs of hex digits
    pairs = [key[i:i+2] for i in range(0, len(key), 2)]
    print(f"Hex pairs: {pairs}")

