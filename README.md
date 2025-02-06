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

