import hashlib
import base58

def sha256(hex_str):
    return hashlib.sha256(bytes.fromhex(hex_str)).digest()

def ripemd160(byte_string):
    ripemd_hash = hashlib.new('ripemd160')
    ripemd_hash.update(byte_string)
    return ripemd_hash.digest()

def hex_to_wif(hex_str, compressed=True):
    # Add version byte (0x80 for mainnet)
    version = "80"
    
    # Ensure the hex string is properly padded
    hex_str = hex_str.zfill(64)
    
    # Add compression flag if needed
    if compressed:
        extended_key = version + hex_str + "01"
    else:
        extended_key = version + hex_str
    
    # Double SHA256
    first_sha = sha256(extended_key)
    second_sha = hashlib.sha256(first_sha).digest()
    
    # First 4 bytes as checksum
    checksum = second_sha[:4].hex()
    
    # Combine everything
    final_key = extended_key + checksum
    
    # Convert to base58
    wif = base58.b58encode(bytes.fromhex(final_key)).decode()
    
    return wif

def get_public_key(private_key_hex, compressed=True):
    try:
        import ecdsa
        signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        
        point_x = verifying_key.pubkey.point.x()
        point_y = verifying_key.pubkey.point.y()
        
        if compressed:
            if point_y % 2 == 0:
                prefix = '02'
            else:
                prefix = '03'
            pub_key_hex = prefix + format(point_x, '064x')
        else:
            prefix = '04'
            pub_key_hex = prefix + format(point_x, '064x') + format(point_y, '064x')
            
        return pub_key_hex
    except Exception as e:
        return f"Error generating public key: {str(e)}"

def pub_key_to_address(pub_key_hex):
    # SHA256
    sha256_hash = sha256(pub_key_hex)
    
    # RIPEMD160
    ripemd160_hash = ripemd160(sha256_hash)
    
    # Add version byte (0x00 for mainnet)
    version_ripemd160_hash = b'\x00' + ripemd160_hash
    
    # Double SHA256 for checksum
    double_sha = hashlib.sha256(hashlib.sha256(version_ripemd160_hash).digest()).digest()
    
    # Add first 4 bytes as checksum
    binary_addr = version_ripemd160_hash + double_sha[:4]
    
    # Convert to base58
    address = base58.b58encode(binary_addr).decode()
    
    return address

# Our private key
private_key = "16230cfcfa9"

print("Private Key Analysis:")
print("=" * 50)
print(f"Private Key (hex): {private_key}")
print(f"Private Key (padded): {private_key.zfill(64)}")

# Generate WIF formats
compressed_wif = hex_to_wif(private_key, compressed=True)
uncompressed_wif = hex_to_wif(private_key, compressed=False)

print("\nWIF Formats:")
print("=" * 50)
print(f"Compressed WIF: {compressed_wif}")
print(f"Uncompressed WIF: {uncompressed_wif}")

# Generate public keys and addresses
compressed_pub = get_public_key(private_key.zfill(64), compressed=True)
uncompressed_pub = get_public_key(private_key.zfill(64), compressed=False)

print("\nPublic Keys:")
print("=" * 50)
print(f"Compressed Pub Key: {compressed_pub}")
print(f"Uncompressed Pub Key: {uncompressed_pub}")

# Generate addresses
compressed_addr = pub_key_to_address(compressed_pub)
uncompressed_addr = pub_key_to_address(uncompressed_pub)

print("\nBitcoin Addresses:")
print("=" * 50)
print(f"Compressed Address: {compressed_addr}")
print(f"Uncompressed Address: {uncompressed_addr}")

# Target address for verification
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
print("\nAddress Verification:")
print("=" * 50)
print(f"Target Address: {target_address}")
print(f"Compressed Match: {compressed_addr == target_address}")
print(f"Uncompressed Match: {uncompressed_addr == target_address}")

