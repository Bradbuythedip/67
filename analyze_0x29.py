import math

# The special value
TARGET_HEX = "29158e29"
target_decimal = int(TARGET_HEX, 16)

# Key components from the pattern
k_rober = int("526f626572", 16)  # "Rober" in hex
r_tdoty = int("74446f7479", 16)  # "tDoty" in hex

# Golden ratio
PHI = (1 + math.sqrt(5)) / 2

def analyze_hex_structure(hex_str):
    # Break into bytes
    bytes_list = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]
    print(f"\nHex structure analysis of {hex_str}:")
    print(f"Bytes: {' '.join(bytes_list)}")
    print(f"Decimal values: {[int(b, 16) for b in bytes_list]}")
    
    # Check for palindrome properties
    if bytes_list == bytes_list[::-1]:
        print("Is a perfect palindrome!")
    
    # Pattern analysis
    print(f"First byte: {bytes_list[0]}")
    print(f"Last byte: {bytes_list[-1]}")
    if bytes_list[0] == bytes_list[-1]:
        print("First and last bytes match!")

def analyze_mathematical_properties(value):
    print(f"\nMathematical analysis of {hex(value)}:")
    
    # Relationship to φ
    phi_power = math.log(value, PHI)
    print(f"Log base φ: {phi_power}")
    
    # Modular properties with name components
    mod_rober = value % k_rober
    mod_tdoty = value % r_tdoty
    print(f"Modulo k_rober: {hex(mod_rober)}")
    print(f"Modulo r_tdoty: {hex(mod_tdoty)}")
    
    # Powers analysis
    print("\nPowers analysis:")
    for i in range(1, 9):
        power_result = pow(0x29, i, 256)  # mod 256 to see byte pattern
        print(f"0x29^{i} mod 256 = {hex(power_result)}")

def fibonacci_check(value):
    # Generate Fibonacci numbers up to the value
    fib = [1, 1]
    while fib[-1] < value:
        fib.append(fib[-1] + fib[-2])
    
    # Find closest Fibonacci numbers
    closest_lower = max([f for f in fib if f <= value])
    closest_higher = min([f for f in fib if f >= value])
    
    print(f"\nFibonacci analysis:")
    print(f"Closest lower Fibonacci: {closest_lower}")
    print(f"Closest higher Fibonacci: {closest_higher}")
    print(f"Distance to lower: {value - closest_lower}")
    print(f"Distance to higher: {closest_higher - value}")

# Perform analysis
print("Analysis of 0x29158e29 pattern")
print("-" * 50)

analyze_hex_structure(TARGET_HEX)
analyze_mathematical_properties(target_decimal)
fibonacci_check(target_decimal)

# Additional analysis of the specific value 0x29
print("\nSpecial analysis of 0x29:")
print(f"0x29 as decimal: {0x29}")
print(f"Binary representation: {bin(0x29)[2:].zfill(8)}")
print(f"Relationship to φ: {0x29/PHI:.4f}")

