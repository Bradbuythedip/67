import math
from datetime import datetime

# Constants
PHI = (1 + math.sqrt(5)) / 2
PATTERN_VALUE = 0x29158e29
PATENT_DATE = datetime(1987, 3, 3).timestamp()
GENESIS_DATE = datetime(2009, 1, 3).timestamp()
TIME_DIFF = int(GENESIS_DATE - PATENT_DATE)

def analyze_time_patterns():
    print("\nTime Component Analysis:")
    print(f"Patent Date: {datetime.fromtimestamp(PATENT_DATE)}")
    print(f"Genesis Date: {datetime.fromtimestamp(GENESIS_DATE)}")
    print(f"Time Difference: {TIME_DIFF} seconds")
    print(f"Time Difference Hex: {hex(TIME_DIFF)}")
    
    # Compare with pattern value
    print(f"\nPattern Value: {hex(PATTERN_VALUE)}")
    print(f"Time diff % Pattern = {hex(TIME_DIFF % PATTERN_VALUE)}")
    
    # Analyze byte structure
    time_bytes = TIME_DIFF.to_bytes(8, 'big')
    pattern_bytes = PATTERN_VALUE.to_bytes(4, 'big')
    
    print("\nByte Structure:")
    print(f"Time bytes: {' '.join(hex(b)[2:].zfill(2) for b in time_bytes)}")
    print(f"Pattern bytes: {' '.join(hex(b)[2:].zfill(2) for b in pattern_bytes)}")
    
    # Look for recurring patterns in time value
    print("\nRecurring Patterns in Time Value:")
    time_hex = hex(TIME_DIFF)[2:].zfill(16)
    for i in range(len(time_hex)-1):
        for j in range(i+2, len(time_hex)+1):
            pattern = time_hex[i:j]
            if time_hex.count(pattern) > 1:
                print(f"Pattern {pattern} occurs multiple times")

def analyze_key_generation_components():
    print("\nKey Generation Component Analysis:")
    
    # Basic components
    components = {
        "0x29": 0x29,
        "0x15": 0x15,
        "0x8e": 0x8e,
        "Pattern": PATTERN_VALUE,
        "Time Diff": TIME_DIFF
    }
    
    # Analyze relationships between components
    print("\nComponent Relationships:")
    for name1, val1 in components.items():
        for name2, val2 in components.items():
            if name1 < name2:  # Avoid duplicates
                ratio = val1 / val2 if val2 != 0 else float('inf')
                print(f"{name1}/{name2} = {ratio}")
                
                # Check if ratio is close to PHI or its powers
                log_phi = math.log(ratio, PHI) if ratio > 0 else 0
                if abs(log_phi - round(log_phi)) < 0.1:
                    print(f"  Close to φ^{round(log_phi)}")
    
    # Look for potential key generation formulas
    print("\nPotential Key Generation Patterns:")
    
    # Test various combinations
    tests = [
        (0x29 * 0x15, "0x29 * 0x15"),
        (0x29 + 0x15, "0x29 + 0x15"),
        (0x29 ^ 0x15, "0x29 ^ 0x15"),
        (0x29 * 0x8e, "0x29 * 0x8e"),
        (PATTERN_VALUE % 0x29, "Pattern % 0x29"),
        (TIME_DIFF % PATTERN_VALUE, "Time_Diff % Pattern")
    ]
    
    for result, formula in tests:
        print(f"{formula} = {hex(result)}")

analyze_time_patterns()
analyze_key_generation_components()

