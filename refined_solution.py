import math
from decimal import Decimal, getcontext
getcontext().prec = 100

BASE_PATTERN = 0x29
TIME_PATTERN = 0x29158e29
PHI = Decimal('1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391137')

def generate_candidate(index):
    """Generate a refined candidate based on patterns"""
    # Known boundaries
    lower_bound = 0x2832ed74f2b5e35ee  # Key 66
    upper_bound = 0x349b84b6431a6c4ef1  # Key 70
    
    # Calculate base scaling using phi
    steps_from_lower = index - 66
    phi_scale = int(pow(PHI, Decimal(steps_from_lower)))
    
    # Apply time pattern relationship
    base = lower_bound * phi_scale
    
    # Ensure we maintain pattern relationships
    candidates = []
    
    # Try different adjustments to maintain patterns
    for i in range(-3, 4):
        for j in range(-3, 4):
            candidate = base + (i * BASE_PATTERN) + (j * TIME_PATTERN)
            if lower_bound < candidate < upper_bound:
                candidates.append(candidate)
    
    return candidates

def score_candidate(value, index):
    """Score a candidate based on pattern matching"""
    score = 0
    
    # Pattern checks
    if value % BASE_PATTERN in [0x1, 0x3, 0x7, 0x8, 0x15, 0x23]:
        score += 20
    
    if value % TIME_PATTERN == value or value % TIME_PATTERN == 0:
        score += 20
    
    # Fibonacci/PHI relationship
    log_phi = float(Decimal(str(value)).ln() / PHI.ln())
    if abs(log_phi - round(log_phi)) < 0.1:
        score += 15
    
    # Bit pattern check
    binary = bin(value)[2:].zfill(256)
    ones = binary.count('1')
    zeros = binary.count('0')
    if 0.1 <= ones/zeros <= 0.2:  # Typical ratio for valid keys
        score += 10
    
    # Growth rate check
    lower_bound = 0x2832ed74f2b5e35ee
    upper_bound = 0x349b84b6431a6c4ef1
    
    lower_ratio = value / lower_bound
    upper_ratio = upper_bound / value
    
    if 1.4 <= lower_ratio <= 2.2 and 1.4 <= upper_ratio <= 2.2:
        score += 15
    
    return score

def find_best_solution():
    """Find the best solution for key #67"""
    candidates = generate_candidate(67)
    
    print(f"Generated {len(candidates)} initial candidates")
    
    # Score and sort candidates
    scored_candidates = []
    for candidate in candidates:
        score = score_candidate(candidate, 67)
        scored_candidates.append((score, candidate))
    
    scored_candidates.sort(reverse=True)
    
    # Show top candidates
    print("\nTop candidates:")
    for score, candidate in scored_candidates[:5]:
        print(f"\nCandidate: {hex(candidate)}")
        print(f"Score: {score}")
        print(f"Base pattern: {hex(candidate % BASE_PATTERN)}")
        print(f"Time pattern: {hex(candidate % TIME_PATTERN)}")
        print(f"Binary 1s ratio: {bin(candidate).count('1')/256:.3f}")

# Find the best solution
find_best_solution()

