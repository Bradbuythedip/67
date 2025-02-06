from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

# Last known values
puzzle_60_hex = "0xfc07a1825367bbe"
puzzle_60_dec = int(puzzle_60_hex, 16)

print(f"Puzzle 60 value: {puzzle_60_hex} ({puzzle_60_dec})")

# Calculate expected value for puzzle 67
steps = 67 - 60
phi_power = pow(PHI, steps)
expected_dec = int(puzzle_60_dec * phi_power)
expected_hex = hex(expected_dec)

print(f"\nExpected value for puzzle 67:")
print(f"Steps from 60: {steps}")
print(f"φ^{steps} ≈ {float(phi_power)}")
print(f"Expected decimal: {expected_dec}")
print(f"Expected hex: {expected_hex}")

print(f"\nOur calculated value:")
our_hex = "0x16230d4937b"
our_dec = int(our_hex, 16)
print(f"Hex: {our_hex}")
print(f"Decimal: {our_dec}")

print(f"\nComparison:")
print(f"Number of digits (expected): {len(str(expected_dec))}")
print(f"Number of digits (ours): {len(str(our_dec))}")
print(f"Length in hex (expected): {len(expected_hex[2:])}")
print(f"Length in hex (ours): {len(our_hex[2:])}")

