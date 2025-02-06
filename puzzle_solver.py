import math
from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants from previous analysis
BASE_PATTERN = 0x29
TIME_PATTERN = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

# Known key-value pairs (index, private_key)
KNOWN_PAIRS = {
    65: 0x1A838B13505B26867,
    66: 0x2832ED74F2B5E35EE,
    70: 0x349B84B6431A6C4EF1,
    75: 0x4C5CE114686A1336E07,
    80: 0xEA1A5C66DCC11B5AD180,
    85: 0x11720C4F018D51B8CEBBA8,
    90: 0x2CE00BB2136A445C71E85BF
}

def analyze_known_keys():
    """Analyze patterns in known keys"""
    print("\nAnalyzing known key patterns:")
    
    # Calculate ratios between consecutive known keys
    indices = sorted(KNOWN_PAIRS.keys())
    for i in range(len(indices)-1):
        idx1, idx2 = indices[i], indices[i+1]
        key1, key2 = KNOWN_PAIRS[idx1], KNOWN_PAIRS[idx2]
        ratio = key2 / key1
        index_diff = idx2 - idx1
        
        print(f"\nBetween indices {idx1} and {idx2} (diff: {index_diff}):")
        print(f"Ratio: {ratio}")
        print(f"Per step: {ratio ** (1/index_diff)}")
        
        # Look for patterns in hex representation
        hex1 = hex(key1)[2:].zfill(64)
        hex2 = hex(key2)[2:].zfill(64)
        print(f"Key {idx1}: {hex1}")
        print(f"Key {idx2}: {hex2}")

def analyze_target_keys():
    """Analyze specific properties of target indices"""
    target_indices = [67, 68, 69, 71, 72, 73, 74]  # Some unknown indices
    
    print("\nAnalyzing target indices:")
    for idx in target_indices:
        print(f"\nIndex {idx}:")
        
        # Find nearest known keys
        lower_key = max((k for k in KNOWN_PAIRS.keys() if k < idx), default=None)
        upper_key = min((k for k in KNOWN_PAIRS.keys() if k > idx), default=None)
        
        if lower_key and upper_key:
            print(f"Between known keys {lower_key} and {upper_key}")
            
            # Calculate expected growth based on known keys
            lower_val = KNOWN_PAIRS[lower_key]
            upper_val = KNOWN_PAIRS[upper_key]
            position_ratio = (idx - lower_key) / (upper_key - lower_key)
            
            # Estimate value using geometric progression
            log_lower = math.log(lower_val)
            log_upper = math.log(upper_val)
            log_estimated = log_lower + (log_upper - log_lower) * position_ratio
            estimated = int(math.exp(log_estimated))
            
            print(f"Estimated value: {hex(estimated)}")
            
            # Check if it follows pattern rules
            mod_base = estimated % BASE_PATTERN
            mod_time = estimated % TIME_PATTERN
            print(f"Base pattern check: {hex(mod_base)}")
            print(f"Time pattern check: {hex(mod_time)}")

def find_key_67():
    """Attempt to find key for index 67"""
    # Known bounds
    lower_idx, upper_idx = 66, 70
    lower_key = KNOWN_PAIRS[66]
    upper_key = KNOWN_PAIRS[70]
    
    # Calculate growth rate
    steps = upper_idx - lower_idx
    growth_rate = (upper_key / lower_key) ** (1/steps)
    
    # Calculate estimated value
    steps_from_lower = 67 - lower_idx
    estimated = int(lower_key * (growth_rate ** steps_from_lower))
    
    # Apply pattern constraints
    base_aligned = estimated + (BASE_PATTERN - (estimated % BASE_PATTERN))
    time_aligned = estimated + (TIME_PATTERN - (estimated % TIME_PATTERN))
    
    # Final candidates
    candidates = [
        estimated,
        base_aligned,
        time_aligned,
        int(estimated * PHI) % 2**256,
        int(estimated / PHI) % 2**256
    ]
    
    print("\nPossible solutions for index 67:")
    for i, candidate in enumerate(candidates):
        print(f"\nCandidate {i+1}:")
        print(f"Value: {hex(candidate)}")
        print(f"Base pattern: {hex(candidate % BASE_PATTERN)}")
        print(f"Time pattern: {hex(candidate % TIME_PATTERN)}")

print("Bitcoin Puzzle Key Analysis")
print("=" * 50)
analyze_known_keys()
analyze_target_keys()
find_key_67()

