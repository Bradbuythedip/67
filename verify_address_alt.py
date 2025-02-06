from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import hashlib
import base58
import binascii

def sha256(data):
    return hashlib.sha256(data).digest()

def ripemd160(data):
    return hashlib.new('ripemd160', data).digest()

def hash160(data):
    return ripemd160(sha256(data))

def private_key_to_wif(private_key_hex, compressed=True):
    # Add leading zeros if needed
    private_key = private_key_hex.zfill(64)
    
    # Convert to bytes
    private_key_bytes = bytes.fromhex(private_key)
    
    # Add version byte
    version = b'\x80'
    extended = version + private_key_bytes
    
    if compressed:
        extended += b'\x01'
    
    # Double SHA256
    checksum = sha256(sha256(extended))[:4]
    
    # Combine and encode
    wif = base58.b58encode(extended + checksum)
    return wif.decode('ascii')

def verify_private_key(private_key_hex, target_address):
    # WIF formats
    compressed_wif = private_key_to_wif(private_key_hex, True)
    uncompressed_wif = private_key_to_wif(private_key_hex, False)
    
    print(f"Private Key: {private_key_hex}")
    print("\nWIF Formats:")
    print(f"Compressed:   {compressed_wif}")
    print(f"Uncompressed: {uncompressed_wif}")
    
    return {
        'compressed_wif': compressed_wif,
        'uncompressed_wif': uncompressed_wif
    }

# Test with our private key
private_key = "2832ed74fa69ee0e4"
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

result = verify_private_key(private_key, target_address)

# Save WIF formats to file for further verification
with open('private_key_wif.txt', 'w') as f:
    f.write(f"Private Key (hex): {private_key}\n")
    f.write(f"Compressed WIF: {result['compressed_wif']}\n")
    f.write(f"Uncompressed WIF: {result['uncompressed_wif']}\n")
    f.write(f"Target Address: {target_address}\n")

print("\nWIF formats have been saved to private_key_wif.txt")
print("You can verify these using a Bitcoin address generator.")

