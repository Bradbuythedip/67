from decimal import Decimal, getcontext
getcontext().prec = 100

# Known values in sequence
KNOWN_VALUES = [
    (52, 0x522b1c52),
    (53, 0x7b40aa7b),
    (54, 0xa45638a4),
    (55, 0x11f96e31f),
    (56, 0x1c3ed1bc3),
    (57, 0x2e383fee2),
    (58, 0x4a7711aa5),
    (59, 0x78af51987),
    (60, 0xc3266342c)
]

print("Analyzing ratios between consecutive values:")
print("=" * 50)

for i in range(len(KNOWN_VALUES)-1):
    curr_num, curr_val = KNOWN_VALUES[i]
    next_num, next_val = KNOWN_VALUES[i+1]
    
    ratio = Decimal(next_val) / Decimal(curr_val)
    print(f"\nFrom puzzle {curr_num} to {next_num}:")
    print(f"Value {curr_num}: 0x{curr_val:x}")
    print(f"Value {next_num}: 0x{next_val:x}")
    print(f"Ratio: {float(ratio):.4f}")
    
    # Calculate expected value using phi
    phi_ratio = pow(Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137'), next_num-curr_num)
    print(f"φ^{next_num-curr_num}: {float(phi_ratio):.4f}")
    print(f"Difference: {float(ratio - phi_ratio):.4f}")

print("\nProjecting to puzzle 67 from puzzle 60:")
print("=" * 50)
last_val = KNOWN_VALUES[-1][1]
steps = 67 - 60
phi = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
phi_power = pow(phi, steps)
projected = int(Decimal(last_val) * phi_power)

print(f"Starting value (60): 0x{last_val:x}")
print(f"Steps to 67: {steps}")
print(f"φ^{steps}: {float(phi_power):.4f}")
print(f"Projected value: 0x{projected:x}")
print(f"Decimal: {projected}")

