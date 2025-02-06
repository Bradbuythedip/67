from bitcoin import *

# Our private key
private_key = "16230cfcfa9"
# Pad to 64 characters
private_key_padded = private_key.zfill(64)

print("Private Key Analysis:")
print("=" * 50)
print(f"Private Key (hex): {private_key}")
print(f"Private Key (padded): {private_key_padded}")

# Generate public keys
pub_key = privtopub(private_key_padded)
pub_key_compressed = compress(pub_key)

print("\nPublic Keys:")
print("=" * 50)
print(f"Uncompressed Public Key: {pub_key}")
print(f"Compressed Public Key: {pub_key_compressed}")

# Generate addresses
address = pubtoaddr(pub_key)
address_compressed = pubtoaddr(pub_key_compressed)

print("\nBitcoin Addresses:")
print("=" * 50)
print(f"Uncompressed Address: {address}")
print(f"Compressed Address: {address_compressed}")

# Generate WIF
wif = encode_privkey(private_key_padded, 'wif')
wif_compressed = encode_privkey(private_key_padded, 'wif_compressed')

print("\nWIF Formats:")
print("=" * 50)
print(f"Uncompressed WIF: {wif}")
print(f"Compressed WIF: {wif_compressed}")

# Target address for verification
target_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"
print("\nAddress Verification:")
print("=" * 50)
print(f"Target Address: {target_address}")
print(f"Compressed Match: {address_compressed == target_address}")
print(f"Uncompressed Match: {address == target_address}")

