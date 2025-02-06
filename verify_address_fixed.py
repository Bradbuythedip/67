from bitcointx.core.key import CPubKey
from bitcointx.wallet import CBitcoinAddress
import hashlib
import base58

def pubkey_to_address(pubkey_hex):
    # Add version byte (0x00 for mainnet)
    version = b'\x00'
    
    # Double SHA256 and RIPEMD160
    sha256_1 = hashlib.sha256(bytes.fromhex(pubkey_hex)).digest()
    ripemd160 = hashlib.new('ripemd160', sha256_1).digest()
    
    # Add version byte
    vh160 = version + ripemd160
    
    # Checksum (double SHA256)
    checksum = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()[:4]
    
    # Combine everything and encode to base58
    final = vh160 + checksum
    address = base58.b58encode(final).decode()
    
    return address

# Our solution
solution = "16230d4937b"
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

print("Verifying solution against target address:")
print(f"Solution (hex): 0x{solution}")
print(f"Target address: {target_address}")
print("\nTrying different hex formats:")

# Try different padding approaches
formats_to_try = [
    solution.zfill(66),  # 33 bytes (compressed public key)
    solution.zfill(130),  # 65 bytes (uncompressed public key)
    solution + "0" * (64 - len(solution)),  # Right padding to 32 bytes
]

for i, hex_format in enumerate(formats_to_try):
    try:
        address = pubkey_to_address(hex_format)
        print(f"\nAttempt {i+1}:")
        print(f"Hex input: {hex_format}")
        print(f"Generated address: {address}")
        print(f"Matches target?: {address == target_address}")
    except Exception as e:
        print(f"\nAttempt {i+1} failed: {str(e)}")

