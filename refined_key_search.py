from bitcoin import *
import math
from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
BASE_PATTERN = 0x29
TIME_PATTERN = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

def try_key_variations(base_key):
    """Try variations of a base key to find the correct one"""
    variations = []
    
    # Base key
    variations.append(base_key)
    
    # Add/subtract pattern values
    for i in range(-3, 4):
        for j in range(-3, 4):
            variation = base_key + (i * BASE_PATTERN) + (j * TIME_PATTERN)
            if variation > 0:
                variations.append(variation)
    
    # Try phi-based variations
    phi_multiplier = int(PHI * 1000000)
    variations.append(base_key * phi_multiplier // 1000000)
    variations.append(base_key * 1000000 // phi_multiplier)
    
    return variations

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
        
        # Check if either matches
        if address_compressed == target_address or address_uncompressed == target_address:
            print(f"\nFound matching key!")
            print(f"Private Key (hex): {private_key}")
            print(f"Uncompressed addr: {address_uncompressed}")
            print(f"Compressed addr:   {address_compressed}")
            print(f"Target addr:       {target_address}")
            return True
            
    except Exception as e:
        pass
    
    return False

def search_for_key():
    target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
    
    # Known bounds
    lower_bound = 0x2832ed74f2b5e35ee  # Key 66
    upper_bound = 0x349b84b6431a6c4ef1  # Key 70
    
    print("Searching for private key...")
    
    # Try variations based on known patterns
    base_candidates = [
        lower_bound * 2 // 1,  # Simple doubling
        lower_bound * 3 // 2,  # 1.5x
        lower_bound * 5 // 3,  # ~1.67x (close to phi)
        lower_bound * 8 // 5,  # Fibonacci ratio
        int(float(Decimal(str(lower_bound)) * PHI)),  # Phi scaling
    ]
    
    for base in base_candidates:
        print(f"\nTrying variations around {hex(base)}")
        variations = try_key_variations(base)
        
        for var in variations:
            if lower_bound < var < upper_bound:  # Check if within bounds
                if verify_key(var, target_address):
                    return var
    
    return None

# Search for the key
result = search_for_key()

if result:
    print("\nFinal verification:")
    private_key = hex(result)[2:].zfill(64)
    print(f"WIF (compressed):   {encode_privkey(private_key, 'wif_compressed')}")
    print(f"WIF (uncompressed): {encode_privkey(private_key, 'wif')}")
else:
    print("\nNo matching key found")

