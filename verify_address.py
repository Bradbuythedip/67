import hashlib
import base58
from binascii import hexlify, unhexlify

def hash160(hex_str):
    sha = hashlib.sha256(unhexlify(hex_str)).digest()
    rip = hashlib.new('ripemd160', sha).digest()
    return rip

def hex_to_address(hex_str, version_byte=0):
    # Add version byte in front of RIPEMD-160 hash
    vh160 = bytes([version_byte]) + hash160(hex_str)
    
    # Add SHA256(SHA256()) hash checksum
    double_sha256 = hashlib.sha256(hashlib.sha256(vh160).digest()).digest()
    
    # Add 4 bytes of checksum
    addr = vh160 + double_sha256[:4]
    
    # Encode in base58
    return base58.b58encode(addr).decode()

# Our solution
solution = "16230d4937b"
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

# Try different padding approaches
print("Verifying solution against target address:")
print(f"Solution (hex): 0x{solution}")
print(f"Target address: {target_address}")
print("\nTrying different hex formats:")

# Test different padding lengths to ensure proper byte alignment
formats_to_try = [
    solution,
    solution.zfill(64),  # Full 32 bytes
    solution + "0" * (64 - len(solution)),  # Right padding
]

for i, hex_format in enumerate(formats_to_try):
    try:
        generated_addr = hex_to_address(hex_format)
        print(f"\nAttempt {i+1}:")
        print(f"Hex input: {hex_format}")
        print(f"Generated address: {generated_addr}")
        print(f"Matches target?: {generated_addr == target_address}")
    except Exception as e:
        print(f"\nAttempt {i+1} failed: {str(e)}")

