# Puzzle 67 Solver

This repository contains scripts for solving Bitcoin puzzle 67 using phi-based calculation and address verification.

## Algorithm Description

The core algorithm is based on several key patterns and mathematical relationships:

1. The values follow a Fibonacci-like growth pattern based on the golden ratio (φ)
2. Each value is related to its puzzle number through a formula involving φ
3. There's a consistent scaling factor multiplied by BASE (0x29)
4. There are additional adjustments based on the puzzle number modulo 3

### Core Formula
```
value = SCALING_FACTOR * φ^n * BASE
where:
- BASE = 0x29 (41 in decimal)
- φ (phi) = 1.618033988749894848... (golden ratio)
- n = (puzzle_number - 51)
- SCALING_FACTOR ≈ 16811670.8537
```

### Known Patterns
Puzzle numbers where n % 3 == 0: value = value XOR BASE
Puzzle numbers where n % 3 == 1: value = value OR BASE

## Scripts

1. `verify_algo.py` - Verifies algorithm against known solutions
2. `verify_bitcoin.py` - Generates and verifies Bitcoin addresses
3. `verify_wif_address.py` - Generates WIF format and verifies addresses
4. `wide_range_search.py` - Parallel search around calculated value

## Usage

1. Calculate base value:
```python
python3 verify_algo.py
```

2. Generate WIF and verify address:
```python
python3 verify_wif_address.py
```

3. Search wide range for correct value:
```python
python3 wide_range_search.py
```

## Current Best Guess
Our current calculated value for puzzle 67: 0x16230cfcfa9

## Dependencies
- python3
- bitcoin
- base58
- coincurve (optional)

## Installation
```bash
pip3 install bitcoin base58 coincurve
```


## Wide Range Search

The `search_wide_range.py` script performs a parallel search around the calculated value:

- Searches ±1 trillion values by default
- Uses 8 parallel processes
- Reports progress in real-time
- Checks both compressed and uncompressed addresses
- Can be interrupted safely with Ctrl+C

To run the wide range search:
```bash
python3 search_wide_range.py
```

The script will search both above and below the calculated value, reporting progress regularly.

## Optimized 28-Thread Scanner

The `puzzle67_scanner.py` script is optimized for CPU scanning using 28 threads:

### Features:
- Uses coincurve for faster key generation
- Optimized address generation with custom functions
- Real-time progress monitoring
- Automatic result saving
- Memory-efficient key handling

### Optimizations:
1. Uses coincurve instead of python-ecdsa for faster key operations
2. Custom Bitcoin address generation without full library overhead
3. Batch processing with progress reporting
4. Efficient memory management
5. Parallel search in both directions from base value

### Usage:
```bash
# Install requirements
pip3 install coincurve base58

# Run scanner
python3 puzzle67_scanner.py
```

### Performance Tips:
1. Adjust RANGE_PER_THREAD based on your CPU speed
2. Monitor CPU usage and adjust thread count if needed
3. Run on a machine with good single-thread performance
4. Keep system cool for sustained performance
5. Consider using PyPy for potential speed improvements


## Pattern Analysis Tools

### New Analysis Scripts:
1. `pattern_analysis.py` - Deep analysis of mathematical patterns
2. `bit_pattern_analysis.py` - Analysis of bit-level patterns
3. `bit_transition.py` - Study of bit transitions between puzzles
4. `relaxed_pattern_search.py` - Refined search with relaxed criteria

### Key Pattern Insights:
1. Phi-based growth with consistent scaling factor
2. Modulo patterns for puzzles where n%3 == 1
3. Bit preservation patterns between consecutive puzzles
4. Transition patterns in bit flips (0->1 and 1->0)

### Search Criteria:
- Base Value (Puzzle 58): 0x4a7711aa5
- Target Preserved Bits: ~50
- Modulo Range: 0x15-0x28
- Expected Ratio: ~76.1034
- Binary Length: 41 bits

### Usage:
```bash
# Run pattern analysis
python3 pattern_analysis.py

# Run bit pattern analysis
python3 bit_pattern_analysis.py

# Run bit transition analysis
python3 bit_transition.py

# Run refined search
python3 relaxed_pattern_search.py
```


## Continuous Search Tool

The `continuous_search.py` script implements a persistent search that:
1. Continuously expands search range until target is found
2. Reports detailed statistics and progress
3. Shows pattern matches along the way
4. Saves solution when found

### Features:
- Real-time progress monitoring
- Performance statistics (keys/second)
- Pattern match analysis
- Automatic result saving
- Expanding range search

### Usage:
```bash
python3 continuous_search.py
```

The script will continue searching in expanding ranges until the target address is found, showing progress and pattern matches along the way.


## Targeted Search Based on Adjacent Puzzles

Analysis of puzzles 66 and 68 revealed crucial patterns:
1. Puzzle 68 is approximately 2x puzzle 66
2. Puzzle 67 should be approximately 1.5x puzzle 66
3. Specific bit transition patterns between consecutive puzzles

New `targeted_search.py` implements these insights:
- Uses puzzles 66 and 68 as boundaries
- Enforces observed bit transition patterns
- Checks ratio relationships
- Verifies modulo constraints

### Usage:
```bash
python3 targeted_search.py
```

The search focuses on the mathematically expected range with tight constraints based on observed patterns in surrounding puzzles.


## Cyclic Pattern Search Based on Puzzle 70 Analysis

Analysis of puzzle 70 revealed critical patterns:
1. Addresses match in compressed format
2. Modulo values follow a cyclic pattern
3. Phi ratios show consistent relationships

New `cyclic_pattern_search.py` implements these insights:
- Uses verified patterns from puzzle 70
- Implements cyclic modulo checking
- Focuses on compressed address format
- Verifies ratio relationships

### Usage:
```bash
python3 cyclic_pattern_search.py
```

The search uses cyclic patterns verified against puzzle 70's known solution.


## Exact Match Search

The `exact_match_search.py` script implements a precise search that:
1. Only checks compressed addresses
2. Immediately stops on exact match with 1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9
3. Shows real-time progress with latest addresses
4. Saves solution with detailed verification

Key Features:
- Fast constraint checking before address generation
- Clear progress display with latest addresses
- Immediate stop on exact match
- Robust error handling
- Detailed solution verification

### Usage:
```bash
python3 exact_match_search.py
```

The script will stop immediately when finding the exact target address.

