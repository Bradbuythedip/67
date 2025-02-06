from decimal import Decimal, getcontext
getcontext().prec = 100

# Constants
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')
BASE = 0x29
SCALING_FACTOR = 16811670.8537

def verify_value(puzzle_number, value):
    n = puzzle_number - 51
    phi_power = int(round(float(pow(PHI, n))))
    ratio = value / (BASE * phi_power)
    return abs(ratio - SCALING_FACTOR)

# Our calculated value
central_value = 0x16230d4937b
range_to_check = 20  # Check 20 values above and below

print(f"Checking values around 0x{central_value:x} for puzzle 67")
print("=" * 50)
print("\nValue               | Deviation from expected ratio")
print("-" * 50)

best_value = central_value
best_deviation = verify_value(67, central_value)

for offset in range(-range_to_check, range_to_check + 1):
    test_value = central_value + offset
    deviation = verify_value(67, test_value)
    
    if deviation < best_deviation:
        best_deviation = deviation
        best_value = test_value
    
    if abs(offset) <= 5:  # Only print values very close to our calculated value
        print(f"0x{test_value:x} | {deviation}")

print("\nBest matching value:")
print(f"0x{best_value:x} with deviation of {best_deviation}")
