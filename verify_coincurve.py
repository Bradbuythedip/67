from coincurve import PublicKey
from hashlib import sha256
import hashlib
import base58

def sha256_ripemd160(x):
    h = hashlib.new('ripemd160')
    h.update(sha256(x).digest())
    return h.digest()

def pubkey_to_address(pubkey_bytes):
    # Get RIPEMD160(SHA256()) hash
    hash160 = sha256_ripemd160(pubkey_bytes)
    
    # Add version byte (0x00 for mainnet addresses)
    version = b'\x00'
    vh160 = version + hash160
    
    # Add checksum
    checksum = sha256(sha256(vh160).digest()).digest()[:4]
    
    # Encode
    addr = base58.b58encode(vh160 + checksum)
    return addr.decode()

# Our solution and target
solution = "16230d4937b"
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

print(f"Solution (hex): 0x{solution}")
print(f"Target address: {target_address}")
print("\nAttempting verification with different formats:")

# Try different formats
try:
    # As a 32-byte private key
    privkey = bytes.fromhex(solution.zfill(64))
    pubkey = PublicKey.from_valid_secret(privkey).format(compressed=True)
    address = pubkey_to_address(pubkey)
    print(f"\nAs private key:")
    print(f"Generated address: {address}")
    print(f"Matches target?: {address == target_address}")
except Exception as e:
    print(f"Private key attempt failed: {str(e)}")

try:
    # As a public key directly
    pubkey_hex = "02" + solution.zfill(64)  # Compressed format
    pubkey = bytes.fromhex(pubkey_hex)
    address = pubkey_to_address(pubkey)
    print(f"\nAs compressed public key:")
    print(f"Generated address: {address}")
    print(f"Matches target?: {address == target_address}")
except Exception as e:
    print(f"Compressed pubkey attempt failed: {str(e)}")

try:
    # As uncompressed public key
    pubkey_hex = "04" + solution.zfill(64) + "0" * 64
    pubkey = bytes.fromhex(pubkey_hex)
    address = pubkey_to_address(pubkey)
    print(f"\nAs uncompressed public key:")
    print(f"Generated address: {address}")
    print(f"Matches target?: {address == target_address}")
except Exception as e:
    print(f"Uncompressed pubkey attempt failed: {str(e)}")

