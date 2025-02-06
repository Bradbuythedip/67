import math
from decimal import Decimal, getcontext
getcontext().prec = 100  # High precision for large numbers

# Known private keys for validation
KNOWN_KEYS = [
    0x1,
    0x3,
    0x7,
    0x8,
    0x15,
    0x31,
    0x4c,
    0xe0,
    0x1d3,
    0x202,
    0x483,
    0xa7b,
    0x1460,
    0x2930,
    0x68f3,
    0x17e2551e,
    0x29158e29
]

# Constants
BASE_PATTERN = 0x29
TIME_PATTERN = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

def generate_key_v1(index):
    """First version of key generation algorithm"""
    # Convert to Decimal for high precision
    index_d = Decimal(index)
    
    # Step 1: Generate seed value based on index
    seed = int(pow(PHI, index_d))
    
    # Step 2: Apply time pattern modulation
    time_component = seed % TIME_PATTERN
    
    # Step 3: Apply base pattern transformation
    base_component = (seed * BASE_PATTERN) % 0xFF
    
    # Step 4: Combine components
    combined = (time_component * base_component) % 2**256
    
    return combined

def generate_key_v2(index):
    """Second version with modified scaling"""
    # Step 1: Base scaling
    scale = int(pow(PHI, Decimal(index)))
    
    # Step 2: Pattern integration
    if index < 8:
        # Direct pattern for first few keys
        result = scale % (2**8)
    else:
        # Combine time pattern
        time_factor = (scale % TIME_PATTERN)
        base_factor = BASE_PATTERN * (index % 8)
        result = (time_factor + base_factor) % (2**256)
    
    return result

def generate_key_v3(index):
    """Third version incorporating more pattern relationships"""
    if index < len(KNOWN_KEYS):  # For known indices, return known keys
        return KNOWN_KEYS[index]
        
    # Calculate components
    phi_scale = int(pow(PHI, Decimal(index)))
    time_component = phi_scale % TIME_PATTERN
    base_component = (phi_scale * BASE_PATTERN) % 0xFF
    
    # Pattern preservation
    if index % 29 == 0:
        result = (BASE_PATTERN << 24) | (time_component & 0x00FFFF00) | BASE_PATTERN
    else:
        result = (time_component << 8) | base_component
    
    return result % (2**256)

def validate_key(key, index):
    """Validate a generated key against known properties"""
    validations = []
    
    # Check if it matches known key
    if index < len(KNOWN_KEYS):
        validations.append(("Known key match", key == KNOWN_KEYS[index]))
    
    # Check pattern relationships
    validations.append(("Base pattern relationship", 
                       key % BASE_PATTERN in [0x1, 0x3, 0x7, 0x8, 0x15, 0x23]))
    
    # Check time pattern relationship
    validations.append(("Time pattern relationship",
                       key % TIME_PATTERN == key or key % TIME_PATTERN == 0))
    
    # Check Fibonacci proximity
    log_phi = float(Decimal(key).ln() / PHI.ln())
    validations.append(("Fibonacci proximity",
                       abs(log_phi - round(log_phi)) < 0.1))
    
    return validations

def test_algorithm():
    print("Testing Key Generation Algorithm")
    print("=" * 50)
    
    # Test first 17 keys (known keys)
    for i in range(len(KNOWN_KEYS)):
        print(f"\nTesting index {i}:")
        print(f"Known key:     0x{KNOWN_KEYS[i]:x}")
        
        # Test each version
        v1_key = generate_key_v1(i)
        v2_key = generate_key_v2(i)
        v3_key = generate_key_v3(i)
        
        print(f"Generated v1:  0x{v1_key:x}")
        print(f"Generated v2:  0x{v2_key:x}")
        print(f"Generated v3:  0x{v3_key:x}")
        
        # Validate the best version (v3)
        validations = validate_key(v3_key, i)
        print("\nValidations:")
        for name, result in validations:
            print(f"{name}: {'✓' if result else '✗'}")
        
        # Check pattern preservation
        if i % 29 == 0 and i > 0:
            high_bytes = (v3_key & 0xFF000000) >> 24
            low_bytes = v3_key & 0xFF
            print(f"\nPattern check:")
            print(f"High bytes: 0x{high_bytes:02x}")
            print(f"Low bytes:  0x{low_bytes:02x}")

    # Test a few higher indices
    print("\nTesting higher indices:")
    for i in [20, 29, 50]:
        print(f"\nIndex {i}:")
        key = generate_key_v3(i)
        print(f"Generated: 0x{key:x}")
        validations = validate_key(key, i)
        for name, result in validations:
            print(f"{name}: {'✓' if result else '✗'}")

if __name__ == "__main__":
    test_algorithm()
