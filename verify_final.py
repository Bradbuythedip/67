import subprocess
import hashlib
import base58

def ripemd160(data):
    proc = subprocess.Popen(['openssl', 'dgst', '-ripemd160', '-binary'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return proc.communicate(data)[0]

def hex_to_address(hex_str):
    # Convert hex to bytes
    try:
        data = bytes.fromhex(hex_str)
    except ValueError:
        return "Invalid hex string"
    
    # SHA256
    sha256 = hashlib.sha256(data).digest()
    
    # RIPEMD160
    ripemd = ripemd160(sha256)
    
    # Add version byte (0x00 for mainnet)
    version_ripemd = b'\x00' + ripemd
    
    # Double SHA256 for checksum
    double_sha = hashlib.sha256(hashlib.sha256(version_ripemd).digest()).digest()
    
    # First 4 bytes are the checksum
    checksum = double_sha[:4]
    
    # Combine version, ripemd hash, and checksum
    binary_address = version_ripemd + checksum
    
    # Convert to base58
    address = base58.b58encode(binary_address).decode()
    
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
    solution.zfill(64),  # 32 bytes
    "02" + solution.zfill(64),  # Compressed public key format
    "04" + solution.zfill(64) + "0" * 64,  # Uncompressed public key format
]

for i, hex_format in enumerate(formats_to_try):
    try:
        address = hex_to_address(hex_format)
        print(f"\nAttempt {i+1}:")
        print(f"Hex input: {hex_format}")
        print(f"Generated address: {address}")
        print(f"Matches target?: {address == target_address}")
    except Exception as e:
        print(f"\nAttempt {i+1} failed: {str(e)}")

