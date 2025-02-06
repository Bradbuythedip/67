def analyze_key_relationships(pattern_value):
    # Sample of early private keys that might show the pattern most clearly
    early_keys = [
        "0000000000000000000000000000000000000000000000000000000000000029",  # Looking for 0x29 pattern
        "0000000000000000000000000000000000000000000000000000000000002915",  # Looking for pattern extension
        "0000000000000000000000000000000000000000000000000000000000158e29",  # Full pattern components
        "0000000000000000000000000000000000000000000000000000000029158e29"   # Complete pattern
    ]
    
    pattern_bytes = [pattern_value[i:i+2] for i in range(0, len(pattern_value), 2)]
    
    print("\nAnalyzing relationships between pattern 0x29158e29 and private keys:")
    print("Pattern bytes:", " ".join(pattern_bytes))
    
    for key in early_keys:
        # Get the last N bytes where N is the length of our pattern
        key_end = key[-len(pattern_value):]
        key_bytes = [key_end[i:i+2] for i in range(0, len(key_end), 2)]
        
        print(f"\nKey ending: {key_end}")
        print(f"Key bytes: {' '.join(key_bytes)}")
        
        # Compare byte patterns
        matches = sum(1 for kb, pb in zip(key_bytes, pattern_bytes) if kb == pb)
        if matches > 0:
            print(f"Matches {matches} bytes with pattern")
            
        # Check for shifted patterns
        for i in range(len(key_bytes) - len(pattern_bytes) + 1):
            window = key_bytes[i:i+len(pattern_bytes)]
            if window == pattern_bytes:
                print(f"Found complete pattern at position {i}")

# Analyze the specific pattern
pattern = "29158e29"
print("Pattern Analysis")
print("-" * 50)
analyze_key_relationships(pattern)

# Additional analysis of mathematical properties
print("\nAdditional Mathematical Properties:")
print("-" * 50)

# Convert pattern to decimal for analysis
pattern_value = int(pattern, 16)

# Check divisibility properties
print(f"\nDivisibility analysis of {pattern}:")
factors = []
for i in range(1, 101):  # Check first 100 numbers
    if pattern_value % i == 0:
        factors.append(i)
print(f"Factors found: {factors}")

# Check relationship to 0x29
base_pattern = 0x29
relationship = pattern_value / base_pattern
print(f"\nRelationship to 0x29:")
print(f"Pattern value / 0x29 = {relationship}")

