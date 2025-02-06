from bitcoin import *
import math
from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
BASE_PATTERN = 0x29
TIME_PATTERN = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

def generate_candidate_keys():
    """Generate candidate keys based on known patterns"""
    # Known keys
    key_66 = 0x2832ed74f2b5e35ee
    key_70 = 0x349b84b6431a6c4ef1
    
    # Calculate step size
    total_steps = 70 - 66
    step_size = (key_70 - key_66) // total_steps
    
    # Generate candidates
    candidates = []
    
    # Base calculation
    base = key_66 + step_size  # For key 67
    
    # Try variations around this base
    variations = [
        base,  # Exact step
        base + BASE_PATTERN,  # Add base pattern
        base - BASE_PATTERN,  # Subtract base pattern
        base + (BASE_PATTERN * step_size),  # Scaled base pattern
        base + TIME_PATTERN % (2**32),  # Add time pattern mod 2^32
        int(Decimal(str(base)) * PHI),  # Multiply by phi
        int(Decimal(str(base)) / PHI),  # Divide by phi
        base + 0x29,  # Add simple pattern
        base * 0x29 % (2**256),  # Multiply by pattern
    ]
    
    # Additional variations based on bit patterns
    for v in variations[:]:  # Copy list to avoid modifying during iteration
        # Try flipping some bits
        candidates.extend([
            v ^ 0x29,  # XOR with pattern
            v | 0x29,  # OR with pattern
            v & ~0x29,  # AND with inverted pattern
        ])
    
    # Add all variations that look reasonable
    for v in variations:
        if key_66 < v < key_70:  # Only include if within bounds
            candidates.append(v)
    
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

def search_for_key():
    target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
    
    print("Generating candidates...")
    candidates = generate_candidate_keys()
    
    print(f"Testing {len(candidates)} candidates...")
    for i, candidate in enumerate(candidates):
        if i % 10 == 0:  # Progress update
            print(f"Testing candidate {i+1}/{len(candidates)}")
        
        if verify_key(candidate, target_address):
            return candidate
    
    return None

# Search for the key
result = search_for_key()

if not result:
    print("\nNo matching key found")

