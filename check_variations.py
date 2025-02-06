from bitcoin import *

def check_value(hex_val):
    # Pad to 64 characters
    private_key = hex_val.zfill(64)
    
    # Generate addresses
    pub = privtopub(private_key)
    pub_compressed = compress(pub)
    addr = pubtoaddr(pub)
    addr_compressed = pubtoaddr(pub_compressed)
    
    return {
        'uncompressed': addr,
        'compressed': addr_compressed,
        'private': private_key
    }

# Base value variations
base_values = [
    0x16230cfcfa9,  # Original
    0x16230cfcfa9 << 1,  # Shifted left
    0x16230cfcfa9 >> 1,  # Shifted right
    0x16230cfcfa9 ^ 0x29,  # XORed with BASE
    0x16230cfcfa9 | 0x29,  # ORed with BASE
    0x16230cfcfa9 + 0x29,  # Added BASE
    0x16230cfcfa9 - 0x29   # Subtracted BASE
]

target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

print("Checking value variations:")
print("=" * 50)

for base in base_values:
    # Check a small range around each variation
    for offset in range(-5, 6):
        test_value = base + offset
        hex_val = hex(test_value)[2:]  # Remove '0x' prefix
        
        try:
            addresses = check_value(hex_val)
            
            print(f"\nTesting 0x{hex_val}:")
            print(f"Uncompressed: {addresses['uncompressed']}")
            print(f"Compressed: {addresses['compressed']}")
            
            if addresses['uncompressed'] == target_address:
                print("MATCH FOUND! (uncompressed)")
                print(f"Private key: {addresses['private']}")
            if addresses['compressed'] == target_address:
                print("MATCH FOUND! (compressed)")
                print(f"Private key: {addresses['private']}")
        except Exception as e:
            print(f"Error with value 0x{hex_val}: {str(e)}")

