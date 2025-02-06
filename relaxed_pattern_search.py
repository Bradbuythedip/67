from bitcoin import *
from decimal import Decimal, getcontext

# Set precision
getcontext().prec = 1000

def check_pattern_match(value, base_value, target_preserved_bits=50):
    """Check if a value matches relaxed criteria"""
    # Convert to binary
    val_bin = bin(value)[2:].zfill(64)
    base_bin = bin(base_value)[2:].zfill(64)
    
    # Count preserved bits (relaxed)
    preserved = sum(1 for a, b in zip(val_bin, base_bin) if a == b)
    if abs(preserved - target_preserved_bits) > 5:  # Relaxed tolerance
        return False
    
    # Check modulo pattern (relaxed range)
    mod = value % 0x29
    if mod < 0x15 or mod > 0x28:  # Wider range
        return False
    
    # Check bit length (exact)
    if len(bin(value)[2:]) != 41:
        return False
    
    # Check ratio (relaxed)
    ratio = Decimal(value) / Decimal(base_value)
    expected_ratio = Decimal('76.1034')
    if abs(ratio - expected_ratio) > Decimal('1.0'):  # Relaxed tolerance
        return False
    
    return True

def analyze_value(value, base_value):
    """Detailed analysis of a value"""
    val_bin = bin(value)[2:].zfill(64)
    base_bin = bin(base_value)[2:].zfill(64)
    
    preserved = sum(1 for a, b in zip(val_bin, base_bin) if a == b)
    mod = value % 0x29
    ratio = Decimal(value) / Decimal(base_value)
    
    # New analysis: look at bit transition patterns
    transitions_01 = sum(1 for a, b in zip(base_bin, val_bin) if a == '0' and b == '1')
    transitions_10 = sum(1 for a, b in zip(base_bin, val_bin) if a == '1' and b == '0')
    
    return {
        'preserved_bits': preserved,
        'modulo': hex(mod),
        'ratio': float(ratio),
        '0->1_transitions': transitions_01,
        '1->0_transitions': transitions_10,
        'binary_length': len(bin(value)[2:])
    }

def verify_address(value):
    """Generate and verify addresses for a value"""
    try:
        hex_val = hex(value)[2:].zfill(64)
        pub = privtopub(hex_val)
        pub_compressed = compress(pub)
        
        addr = pubtoaddr(pub)
        addr_compressed = pubtoaddr(pub_compressed)
        
        return addr, addr_compressed
    except:
        return None, None

# Constants
BASE_VALUE = 0x4a7711aa5  # Puzzle 58 value
TARGET_ADDRESS = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
CURRENT_GUESS = 0x16230cfcf80

print("Starting relaxed pattern search...")
print("=" * 70)

# Search around our current guess with wider range
search_range = 50000
matches_found = 0

for offset in range(-search_range, search_range + 1):
    test_value = CURRENT_GUESS + offset
    
    if check_pattern_match(test_value, BASE_VALUE):
        analysis = analyze_value(test_value, BASE_VALUE)
        addr_uncomp, addr_comp = verify_address(test_value)
        
        if addr_uncomp == TARGET_ADDRESS or addr_comp == TARGET_ADDRESS:
            print(f"\nMATCH FOUND!")
            print(f"Value: 0x{test_value:x}")
            print(f"Uncompressed: {addr_uncomp}")
            print(f"Compressed: {addr_comp}")
            print("\nPattern Analysis:")
            print(f"Preserved bits: {analysis['preserved_bits']}")
            print(f"Modulo: {analysis['modulo']}")
            print(f"Ratio: {analysis['ratio']:.4f}")
            print(f"0->1 transitions: {analysis['0->1_transitions']}")
            print(f"1->0 transitions: {analysis['1->0_transitions']}")
            break
        
        matches_found += 1
        if matches_found % 5 == 0:
            print(f"\nPattern match {matches_found} at offset {offset:+d}:")
            print(f"Value: 0x{test_value:x}")
            print(f"Addresses:")
            print(f"  Uncompressed: {addr_uncomp}")
            print(f"  Compressed: {addr_comp}")
            print("\nPattern Analysis:")
            print(f"Preserved bits: {analysis['preserved_bits']}")
            print(f"Modulo: {analysis['modulo']}")
            print(f"Ratio: {analysis['ratio']:.4f}")
            print(f"0->1 transitions: {analysis['0->1_transitions']}")
            print(f"1->0 transitions: {analysis['1->0_transitions']}")

print(f"\nSearch complete. Found {matches_found} pattern matches.")

