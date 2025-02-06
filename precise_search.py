from decimal import Decimal, getcontext
getcontext().prec = 1000  # Much higher precision

# More precise φ
PHI = Decimal('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410443207713449470495658467885098743394422125448770664780915884607499887124007652170575179788341662562494075890697040002812104276217711177780531531714101170466659914669798731761356006708748071013179523689427521948435305678300228785699782977834784587822891109762500302696156170025046433824377648610283831268330372429267526311653392473167111211588186385133162038400522216579128667529465490681131715993432359734949850904094762132229810172610705961164562990981629055520852479035240602017279974717534277759277862561943208275051312181562855122248093947123414517022373580577278616008688382952304592647878017889921990270776903895321968198615143780314997411069260886742962267575605231727775203536139362')

# Constants
BASE = 0x29
SCALING_FACTOR = Decimal('16811670.8537')

def calculate_value(puzzle_number):
    """Calculate value for a given puzzle number"""
    n = puzzle_number - 51
    phi_power = pow(PHI, n)
    
    # Calculate base value
    value = int(SCALING_FACTOR * phi_power * BASE)
    
    # Apply pattern adjustments
    if puzzle_number % 3 == 0:
        value = value ^ BASE
    elif puzzle_number % 3 == 1:
        value = value | BASE
    
    return value

def search_range(center_value, range_size=1000):
    """Search around a value for better matches"""
    results = []
    for offset in range(-range_size, range_size + 1):
        test_value = center_value + offset
        results.append((test_value, hex(test_value)))
    return results

# Known values for verification
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

print("Verifying known values with high precision:")
print("=" * 50)

for puzzle_num, known_value in KNOWN_VALUES:
    calculated = calculate_value(puzzle_num)
    
    print(f"\nPuzzle {puzzle_num}:")
    print(f"Known:      0x{known_value:x}")
    print(f"Calculated: 0x{calculated:x}")
    print(f"Difference: {abs(calculated - known_value)}")
    if abs(calculated - known_value) < 1000:
        print("VERY CLOSE! (< 1000 difference)")

print("\nCalculating puzzle 67:")
print("=" * 50)

# Calculate base value for 67
base_value = calculate_value(67)
print(f"Base calculated value: 0x{base_value:x}")

# Search around this value
print("\nSearching nearby values:")
nearby_values = search_range(base_value, 100)  # Search 100 values up and down

# Print the closest values
print("\nNearest values:")
for i, (value, hex_value) in enumerate(nearby_values[:10]):  # Show first 10 options
    print(f"Option {i+1}: {hex_value}")

