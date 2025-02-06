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
        'compressed': addr_compressed
    }

# Our base value
base_value = 0x16230cfcfa9
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

print("Checking values around 0x16230cfcfa9:")
print("=" * 50)

# Check 10 values above and below
for offset in range(-10, 11):
    test_value = base_value + offset
    hex_val = hex(test_value)[2:]  # Remove '0x' prefix
    addresses = check_value(hex_val)
    
    print(f"\nTesting 0x{hex_val}:")
    print(f"Uncompressed: {addresses['uncompressed']}")
    print(f"Compressed: {addresses['compressed']}")
    
    if addresses['uncompressed'] == target_address:
        print("MATCH FOUND! (uncompressed)")
    if addresses['compressed'] == target_address:
        print("MATCH FOUND! (compressed)")

