from bitcoin import *
import math
from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

# Known key pairs (index, key)
KNOWN_KEYS = {
    65: 0x1A838B13505B26867,
    66: 0x2832ED74F2B5E35EE,
    70: 0x349B84B6431A6C4EF1,
    75: 0x4C5CE114686A1336E07,
    80: 0xEA1A5C66DCC11B5AD180,
    85: 0x11720C4F018D51B8CEBBA8,
    90: 0x2CE00BB2136A445C71E85BF
}

def analyze_key_pattern():
    """Analyze the pattern between known keys"""
    indices = sorted(KNOWN_KEYS.keys())
    patterns = []
    
    for i in range(len(indices)-1):
        idx1, idx2 = indices[i], indices[i+1]
        key1, key2 = KNOWN_KEYS[idx1], KNOWN_KEYS[idx2]
        
        # Calculate various relationships
        diff = key2 - key1
        ratio = key2 / key1
        steps = idx2 - idx1
        step_ratio = ratio ** (1/steps)
        
        patterns.append({
            'indices': (idx1, idx2),
            'diff': diff,
            'ratio': ratio,
            'step_ratio': step_ratio,
            'step_size': diff // steps
        })
        
        print(f"\nBetween indices {idx1} and {idx2}:")
        print(f"Difference: {hex(diff)}")
        print(f"Ratio: {ratio}")
        print(f"Steps: {steps}")
        print(f"Step ratio: {step_ratio}")
    
    return patterns

def generate_key_67_candidates(patterns):
    """Generate candidates for key 67 based on patterns"""
    candidates = []
    
    # Base key (key 66)
    base_key = KNOWN_KEYS[66]
    
    # Use patterns to generate candidates
    for pattern in patterns:
        if pattern['indices'][0] <= 66 and pattern['indices'][1] >= 67:
            # Linear progression
            candidates.append(base_key + pattern['step_size'])
            
            # Geometric progression
            candidates.append(int(base_key * pattern['step_ratio']))
            
            # Phi-based progression
            candidates.append(int(base_key * float(PHI)))
            
            # Pattern-based adjustments
            candidates.append(base_key + (pattern['diff'] // (pattern['indices'][1] - pattern['indices'][0])))
    
    # Add special pattern cases
    candidates.extend([
        base_key + 0x29,  # Add simple pattern
        base_key * 0x29 % (2**256),  # Multiply by pattern
        base_key + 0x29158e29 % (2**32),  # Add time pattern
        int(Decimal(str(base_key)) * PHI),  # Multiply by phi
    ])
    
    return candidates

def verify_key(private_key_int, target_address):
    """Verify if a private key generates the target address"""
    # Convert to hex and pad
    private_key = hex(private_key_int)[2:].zfill(64)
    
    try:
        # Generate public keys
        public_key_uncompressed = privtopub(private_key)
        public_key_compressed = compress(public_key_uncompressed)
        
        # Generate addresses
        address_uncompressed = pubtoaddr(public_key_uncompressed)
        address_compressed = pubtoaddr(public_key_compressed)
        
        if address_compressed == target_address or address_uncompressed == target_address:
            print(f"\nFound matching key!")
            print(f"Private Key (hex): {private_key}")
            print(f"Private Key (int): {private_key_int}")
            print(f"Uncompressed addr: {address_uncompressed}")
            print(f"Compressed addr:   {address_compressed}")
            print(f"Target addr:       {target_address}")
            
            # Generate WIF formats
            wif_c = encode_privkey(private_key, 'wif_compressed')
            wif_u = encode_privkey(private_key, 'wif')
            print(f"\nWIF (compressed):   {wif_c}")
            print(f"WIF (uncompressed): {wif_u}")
            
            return True
            
    except Exception as e:
        pass
    
    return False

# Analyze patterns
print("Analyzing key patterns...")
patterns = analyze_key_pattern()

# Generate candidates for key 67
print("\nGenerating candidates for key 67...")
candidates = generate_key_67_candidates(patterns)

# Test candidates
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
print(f"\nTesting {len(candidates)} candidates...")

for i, candidate in enumerate(candidates):
    if i % 5 == 0:  # Progress update
        print(f"Testing candidate {i+1}/{len(candidates)}")
    
    # Only test if within reasonable bounds
    if KNOWN_KEYS[66] < candidate < KNOWN_KEYS[70]:
        if verify_key(candidate, target_address):
            break

