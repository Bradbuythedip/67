import hashlib
import base58
import binascii

def hex_to_bytes(hex_str):
    return binascii.unhexlify(hex_str.zfill(64))

def get_wif(private_key_hex, compressed=True):
    # Add version byte (0x80 for mainnet)
    version = b'\x80'
    
    # Convert private key to bytes
    private_key_bytes = hex_to_bytes(private_key_hex)
    
    # Create extended key bytes
    extended = version + private_key_bytes
    
    # Add compression flag if needed
    if compressed:
        extended += b'\x01'
    
    # Double SHA256
    first_hash = hashlib.sha256(extended).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    
    # Add checksum
    final_bytes = extended + second_hash[:4]
    
    # Base58 encode
    wif = base58.b58encode(final_bytes).decode('utf-8')
    
    return wif

def verify_address_from_pubkey(pubkey_hex, compressed=True):
    """Generate Bitcoin address from public key"""
    # Convert hex public key to bytes
    pubkey_bytes = binascii.unhexlify(pubkey_hex)
    
    # Perform SHA-256
    sha256_hash = hashlib.sha256(pubkey_bytes).digest()
    
    # Perform RIPEMD-160
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    
    # Add version byte
    version_ripemd160_hash = b'\x00' + ripemd160_hash
    
    # Perform double SHA-256 for checksum
    double_sha256 = hashlib.sha256(hashlib.sha256(version_ripemd160_hash).digest()).digest()
    
    # Add first 4 bytes as checksum
    binary_address = version_ripemd160_hash + double_sha256[:4]
    
    # Encode in base58
    address = base58.b58encode(binary_address).decode('utf-8')
    
    return address

# The private key we want to verify
private_key = "2832ed74fa69ee0e4"

print(f"Private Key: {private_key}")
print("\nWIF formats:")
print(f"Compressed:   {get_wif(private_key, True)}")
print(f"Uncompressed: {get_wif(private_key, False)}")

