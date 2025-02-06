import math
from collections import defaultdict

# Constants
PHI = (1 + math.sqrt(5)) / 2
BASE_PATTERN = 0x29
TIME_PATTERN = 0x29158e29

# Key sequence to analyze
keys = [
    0x1, 0x3, 0x7, 0x8, 0x15, 0x31, 0x4c, 0xe0,
    0x1d3, 0x202, 0x483, 0xa7b, 0x1460, 0x2930, 0x68f3,
    0x17e2551e, 0x29158e29
]

def analyze_differences():
    print("\nAnalyzing differences between consecutive keys:")
    for i in range(len(keys)-1):
        diff = keys[i+1] - keys[i]
        ratio = keys[i+1] / keys[i]
        print(f"Keys {i}->{i+1}:")
        print(f"  Difference: {hex(diff)}")
        print(f"  Ratio: {ratio:.4f}")
        print(f"  Ratio/φ: {ratio/PHI:.4f}")

def analyze_bit_patterns():
    print("\nAnalyzing bit patterns:")
    for i, key in enumerate(keys):
        binary = bin(key)[2:].zfill(32)  # Convert to binary, pad to 32 bits
        ones = binary.count('1')
        zeros = binary.count('0')
        print(f"\nKey {i} ({hex(key)}):")
        print(f"  Binary: {binary}")
        print(f"  1s: {ones}, 0s: {zeros}")
        print(f"  Ratio 1s/0s: {ones/zeros if zeros else 'inf':.4f}")

def find_recurring_patterns():
    print("\nLooking for recurring hex patterns:")
    patterns = defaultdict(list)
    
    for i, key in enumerate(keys):
        hex_str = hex(key)[2:].zfill(64)  # Pad to full 64 hex chars
        # Look for patterns of length 2-8 hex chars
        for length in range(2, 9):
            for start in range(len(hex_str) - length + 1):
                pattern = hex_str[start:start+length]
                patterns[pattern].append(i)
    
    # Show patterns that appear multiple times
    significant_patterns = {k: v for k, v in patterns.items() if len(v) > 1}
    for pattern, occurrences in significant_patterns.items():
        if any(p in pattern for p in ['29', '15', '8e']):  # Focus on patterns related to our target
            print(f"Pattern {pattern} appears in keys: {occurrences}")

def analyze_modular_properties():
    print("\nAnalyzing modular properties:")
    special_mods = [0x29, 0x15, 0x8e, TIME_PATTERN]
    
    for i, key in enumerate(keys):
        print(f"\nKey {i} ({hex(key)}):")
        for mod in special_mods:
            result = key % mod
            print(f"  mod 0x{mod:x} = 0x{result:x}")

def fibonacci_relationship():
    print("\nAnalyzing Fibonacci relationships:")
    # Generate Fibonacci sequence up to largest key
    fib = [1, 1]
    while fib[-1] < max(keys):
        fib.append(fib[-1] + fib[-2])
    
    for i, key in enumerate(keys):
        # Find closest Fibonacci numbers
        lower = max([f for f in fib if f <= key])
        higher = min([f for f in fib if f >= key])
        print(f"\nKey {i} ({hex(key)}):")
        print(f"  Between Fib numbers: {lower} and {higher}")
        print(f"  Distances: -{key-lower}, +{higher-key}")
        print(f"  Ratio to φ^n: {math.log(key, PHI) if key > 0 else 0:.4f}")

print("Comprehensive Key Generation Pattern Analysis")
print("=" * 50)
analyze_differences()
analyze_bit_patterns()
find_recurring_patterns()
analyze_modular_properties()
fibonacci_relationship()

