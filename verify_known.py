from bitcoin import *

# Known solutions to verify (puzzle number, private key, address)
KNOWN_SOLUTIONS = [
    (52, "000000000000000000000000000000000000000000000000000efae164cb9e3c", "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim"),
    (53, "00000000000000000000000000000000000000000000000000180788e47e326c", "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT"),
    (54, "00000000000000000000000000000000000000000000000000236fb6d5ad1f43", "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy"),
    (55, "000000000000000000000000000000000000000000000000006abe1f9b67e114", "1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa"),
    (56, "000000000000000000000000000000000000000000000000009d18b63ac4ffdf", "17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi"),
    (57, "00000000000000000000000000000000000000000000000001eb25c90795d61c", "15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz"),
    (58, "00000000000000000000000000000000000000000000000002c675b852189a21", "1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf"),
    (59, "00000000000000000000000000000000000000000000000007496cbb87cab44f", "1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt"),
    (60, "0000000000000000000000000000000000000000000000000fc07a1825367bbe", "1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su")
]

# Our calculated solution
our_solution = "16230d4937b"
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"

print("Verifying known solutions first:")
print("=" * 50)

for puzzle_num, priv_key, known_addr in KNOWN_SOLUTIONS:
    try:
        # Generate public key and address from private key
        pub = privtopub(priv_key)
        addr = pubtoaddr(pub)
        
        print(f"\nPuzzle {puzzle_num}:")
        print(f"Private key: {priv_key}")
        print(f"Known address:   {known_addr}")
        print(f"Generated addr:  {addr}")
        print(f"Match?: {addr == known_addr}")
        
        # Show the decimal value of the private key
        dec_value = int(priv_key, 16)
        print(f"Decimal value: {dec_value}")
        
    except Exception as e:
        print(f"Error processing puzzle {puzzle_num}: {str(e)}")

print("\nAnalyzing pattern in working solutions:")
print("=" * 50)

# Convert our solution to similar format as known solutions
print(f"Our calculated solution: {our_solution}")
print(f"Target address: {target_address}")

# Try padding our solution to match format
padded_solution = our_solution.zfill(64)
print(f"\nPadded to 64 chars: {padded_solution}")

try:
    pub = privtopub(padded_solution)
    addr = pubtoaddr(pub)
    print(f"Generated address: {addr}")
    print(f"Matches target?: {addr == target_address}")
except Exception as e:
    print(f"Error with our solution: {str(e)}")

