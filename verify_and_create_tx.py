from Cryptodome.Hash import SHA256
import binascii

# Our calculated solution and the provided one
calculated_hex = "0x16230d4937b"
puzzle_params = (67, None, "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9", 147573952589676412927, None, None)

# Convert and compare
calculated_decimal = int(calculated_hex, 16)
given_decimal = puzzle_params[3]

print("Solution Verification:")
print("=" * 50)
print(f"Calculated (hex): {calculated_hex}")
print(f"Calculated (dec): {calculated_decimal}")
print(f"Given (dec): {given_decimal}")
print(f"Given (hex): {hex(given_decimal)}")
print(f"Match?: {calculated_decimal == given_decimal}")

# Transaction Parameters
amount_btc = 6.6
fee_rate = 1000  # sats/vB
recipient = puzzle_params[2]

print("\nTransaction Parameters:")
print("=" * 50)
print(f"Recipient: {recipient}")
print(f"Amount: {amount_btc} BTC")
print(f"Fee Rate: {fee_rate} sats/vB")
print(f"RBF: Disabled")

# Create a basic transaction template
tx_template = {
    "version": 1,
    "locktime": 0,
    "vin": [{
        "txid": hex(given_decimal)[2:].zfill(64),
        "vout": 0,
        "sequence": 0xffffffff  # RBF disabled
    }],
    "vout": [{
        "value": amount_btc * 100000000,  # in satoshis
        "address": recipient
    }]
}

print("\nTransaction Template:")
print("=" * 50)
print(f"Input TXID: {tx_template['vin'][0]['txid']}")
print(f"Input vout: {tx_template['vin'][0]['sequence']}")
print(f"Output address: {tx_template['vout'][0]['address']}")
print(f"Output amount (sats): {int(tx_template['vout'][0]['value'])}")

