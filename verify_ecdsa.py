import hashlib
import ecdsa
import base58

def privatekey_to_address(private_key_hex):
    # Convert to signing key
    signing_key = ecdsa.SigningKey.from_string(bytes.fromhex(private_key_hex), curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    
    # Get public key
    public_key_bytes = verifying_key.to_string()
    public_key_hex = '04' + public_key_bytes.hex()
    
    # Perform SHA-256 hashing on the public key
    sha256_hash = hashlib.sha256(bytes.fromhex(public_key_hex)).digest()
    
    # Perform RIPEMD-160 hashing on the result of SHA-256
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    ripemd160_hash = ripemd160_hash.digest()
    
    # Add version byte in front (0x00 for mainnet)
    version_ripemd160_hash = b'\x00' + ripemd160_hash
    
    # Perform double SHA-256 hashing on the result
    double_sha256_hash = hashlib.sha256(hashlib.sha256(version_ripemd160_hash).digest()).digest()
    
    # First 4 bytes of the second SHA-256 will be used as checksum
    checksum = double_sha256_hash[:4]
    
    # Add the 4 checksum bytes to the version+ripemd160 hash
    binary_address = version_ripemd160_hash + checksum
    
    # Convert to base58 string
    address = base58.b58encode(binary_address).decode('utf-8')
    
    return address

# Known solutions to verify
KNOWN_SOLUTIONS = [
    (52, "000000000000000000000000000000000000000000000000000efae164cb9e3c", "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim"),
    (53, "00000000000000000000000000000000000000000000000000180788e47e326c", "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT"),
    (54, "00000000000000000000000000000000000000000000000000236fb6d5ad1f43", "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy")
]

print("Verifying known solutions:")
print("=" * 50)

for puzzle_num, priv_key, known_addr in KNOWN_SOLUTIONS:
    try:
        generated_addr = privatekey_to_address(priv_key)
        print(f"\nPuzzle {puzzle_num}:")
        print(f"Private key: {priv_key}")
        print(f"Known addr:    {known_addr}")
        print(f"Generated addr: {generated_addr}")
        print(f"Match?: {generated_addr == known_addr}")
    except Exception as e:
        print(f"Error with puzzle {puzzle_num}: {str(e)}")

# Our solution
our_solution = "16230d4937b"
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

print("\nChecking our solution:")
print("=" * 50)
padded_solution = our_solution.zfill(64)
print(f"Original: {our_solution}")
print(f"Padded:   {padded_solution}")

try:
    generated_addr = privatekey_to_address(padded_solution)
    print(f"Generated addr: {generated_addr}")
    print(f"Target addr:    {target_address}")
    print(f"Match?: {generated_addr == target_address}")
except Exception as e:
    print(f"Error with our solution: {str(e)}")

