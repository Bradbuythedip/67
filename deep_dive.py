from decimal import Decimal, getcontext
getcontext().prec = 1000

# Constants
PHI = Decimal('1.6180339887498948482045868343656381177203091798057628621354486227052604628189024497072072041893911374847540880753868917521266338622235369317931800607667263544333890865959395829056383226613199282902678806752087668925017116962070322210432162695486262963136144381497587012203408058879544547492461856953648644492410443207713449470495658467885098743394422125448770664780915884607499887124007652170575179788341662562494075890697040002812104276217711177780531531714101170466659914669798731761356006708748071013179523689427521948435305678300228785699782977834784587822891109762500302696156170025046433824377648610283831268330372429267526311653392473167111211588186385133162038400522216579128667529465490681131715993432359734949850904094762132229810172610705961164562990981629055520852479035240602017279974717534277759277862561943208275051312181562855122248093947123414517022373580577278616008688382952304592647878017889921990270776903895321968198615143780314997411069260886742962267575605231727775203536139362')
BASE = 0x29
SCALING_FACTOR = Decimal('16811670.8537')

KNOWN_SOLUTIONS = [
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

def analyze_bits(value):
    """Analyze bit patterns in a value"""
    bits = bin(value)[2:]  # Remove '0b' prefix
    bit_count = bits.count('1')
    leading_zeros = len(bits) - len(bits.lstrip('0'))
    return {
        'length': len(bits),
        'ones': bit_count,
        'zeros': len(bits) - bit_count,
        'leading_zeros': leading_zeros,
        'pattern': bits[:16] + "..." + bits[-16:] if len(bits) > 32 else bits
    }

def analyze_base_relationship(value):
    """Analyze relationship with BASE"""
    div = value // BASE
    mod = value % BASE
    return {
        'division': hex(div),
        'modulo': hex(mod),
        'div_bits': bin(div).count('1'),
        'mod_bits': bin(mod).count('1')
    }

print("Deep Pattern Analysis of Known Solutions:")
print("=" * 70)

for puzzle_num, known_value in KNOWN_SOLUTIONS:
    n = puzzle_num - 51
    phi_power = pow(PHI, n)
    calculated = int(SCALING_FACTOR * phi_power * BASE)
    
    print(f"\nPuzzle {puzzle_num}:")
    print("-" * 40)
    
    # Basic value analysis
    print(f"Known:      0x{known_value:x}")
    print(f"Calculated: 0x{calculated:x}")
    diff = abs(calculated - known_value)
    print(f"Diff:       0x{diff:x}")
    
    # Bit pattern analysis
    known_bits = analyze_bits(known_value)
    calc_bits = analyze_bits(calculated)
    print("\nBit Analysis:")
    print(f"Known  - Length: {known_bits['length']}, Ones: {known_bits['ones']}, Pattern: {known_bits['pattern']}")
    print(f"Calc   - Length: {calc_bits['length']}, Ones: {calc_bits['ones']}, Pattern: {calc_bits['pattern']}")
    
    # BASE relationship
    known_base = analyze_base_relationship(known_value)
    calc_base = analyze_base_relationship(calculated)
    print("\nBASE (0x29) Relationship:")
    print(f"Known  - Div: {known_base['division']}, Mod: {known_base['modulo']}")
    print(f"Calc   - Div: {calc_base['division']}, Mod: {calc_base['modulo']}")
    
    # Phi relationship
    actual_ratio = Decimal(known_value) / (BASE * phi_power)
    calc_ratio = Decimal(calculated) / (BASE * phi_power)
    print("\nPhi Relationships:")
    print(f"Known value / (BASE * φ^{n}): {float(actual_ratio):.10f}")
    print(f"Calc value / (BASE * φ^{n}):  {float(calc_ratio):.10f}")
    
    # Special patterns
    print("\nSpecial Patterns:")
    print(f"Puzzle mod 3: {puzzle_num % 3}")
    if puzzle_num % 3 == 0:
        print(f"XOR with BASE: 0x{(known_value ^ BASE):x}")
    elif puzzle_num % 3 == 1:
        print(f"OR with BASE: 0x{(known_value | BASE):x}")

print("\nProjecting Pattern to Puzzle 67:")
print("=" * 70)
n = 67 - 51
phi_power = pow(PHI, n)
projected = int(SCALING_FACTOR * phi_power * BASE)

print(f"\nProjected base value: 0x{projected:x}")
projected_bits = analyze_bits(projected)
print(f"\nBit pattern: {projected_bits['pattern']}")
print(f"Length: {projected_bits['length']}, Ones: {projected_bits['ones']}")

base_rel = analyze_base_relationship(projected)
print(f"\nBASE relationship:")
print(f"Division: {base_rel['division']}")
print(f"Modulo: {base_rel['modulo']}")

print(f"\nPuzzle 67 mod 3: {67 % 3}")
if 67 % 3 == 0:
    print(f"Should apply XOR with BASE")
elif 67 % 3 == 1:
    print(f"Should apply OR with BASE")

