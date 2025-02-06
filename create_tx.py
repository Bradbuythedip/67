from Cryptodome.Hash import SHA256
import binascii

# Transaction Parameters
input_address = "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9"  # Address holding the funds
output_address = "32t2YSK116ietMuRD7UoMjW7aBdy5SKh5Y"  # Destination address
amount_btc = 6.6
fee_rate = 1000  # sats/vB
solution_hex = "0x16230d4937b"

# Create a basic transaction template
tx_template = {
    "version": 1,
    "locktime": 0,
    "vin": [{
        "address": input_address,
        "amount": amount_btc,
        "sequence": 0xffffffff  # RBF disabled
    }],
    "vout": [{
        "value": amount_btc * 100000000,  # in satoshis
        "address": output_address
    }]
}

print("Transaction Template for MARA:")
print("=" * 50)
print(f"Input Address: {input_address}")
print(f"Output Address: {output_address}")
print(f"Amount: {amount_btc} BTC")
print(f"Fee Rate: {fee_rate} sats/vB")
print(f"RBF: Disabled")
print(f"Solution used: {solution_hex}")
print("\nTransaction Details:")
print("-" * 50)
print(f"Input value (sats): {int(tx_template['vout'][0]['value'])}")
print(f"Sequence (No RBF): {hex(tx_template['vin'][0]['sequence'])}")

print("\nMARA CLI Command:")
print("-" * 50)
command = f"""mara-cli createrawtransaction '''
[{{
  "txid": "{solution_hex[2:]}000000000000000000000000000000000000000000000000",
  "vout": 0,
  "address": "{input_address}",
  "amount": {amount_btc}
}}]''' '''
[{{
  "{output_address}": {amount_btc}
}}]''' 0 false"""
print(command)

