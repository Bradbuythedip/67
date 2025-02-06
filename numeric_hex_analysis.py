from decimal import Decimal, getcontext
getcontext().prec = 100

# Known private keys
known_keys = [
    (52, '00000000000000000000000000000000000000000000000000efae164cb9e3c'),
    (53, '00000000000000000000000000000000000000000000000000180788e47e326c'),
    (54, '00000000000000000000000000000000000000000000000000236fb6d5ad1f43'),
    (55, '00000000000000000000000000000000000000000000000000006abe1f9b67e114'),
    (56, '000000000000000000000000000000000000000000000000009d18b63ac4ffdf'),
    (57, '0000000000000000000000000000000000000000000000001eb25c90795d61c'),
    (58, '0000000000000000000000000000000000000000000000002c675b852189a21'),
    (59, '00000000000000000000000000000000000000000000000007496cbb87cab44f'),
    (60, '00000000000000000000000000000000000000000000000fc07a1825367bbe')
]

def analyze_numeric_pattern():
    print("Analyzing Numeric Pattern in Hex Values:")
    print("=" * 50)
    
    # Extract actual numeric values (removing leading zeros)
    values = [(num, int(key.lstrip('0'), 16)) for num, key in known_keys]
    
    for i, (puzzle, value) in enumerate(values):
        print(f"\nPuzzle {puzzle}:")
        hex_str = hex(value)[2:] # Remove '0x' prefix
        print(f"Value: {hex_str}")
        print(f"Length: {len(hex_str)} hex digits")
        
        # Look for patterns in the digits themselves
        first_digits = hex_str[:2]
        last_digits = hex_str[-2:]
        print(f"First digits: {first_digits}")
        print(f"Last digits: {last_digits}")
        
        if i > 0:
            prev_puzzle, prev_value = values[i-1]
            ratio = value / prev_value
            print(f"Ratio to previous: {ratio:.4f}")
            
            # Look at digit-by-digit changes
            prev_hex = hex(prev_value)[2:].zfill(len(hex_str))
            print("Digit changes:", end=' ')
            for j, (curr, prev) in enumerate(zip(hex_str, prev_hex)):
                if curr != prev:
                    print(f"pos {j}: {prev}->{curr}", end=', ')
            print()

def find_numeric_progression():
    """Analyze the numeric progression of the values"""
    print("\nAnalyzing Numeric Progression:")
    print("=" * 50)
    
    values = [(num, int(key.lstrip('0'), 16)) for num, key in known_keys]
    
    # Look at differences between consecutive values
    for i in range(len(values)-1):
        curr_puzzle, curr_val = values[i]
        next_puzzle, next_val = values[i+1]
        
        diff = next_val - curr_val
        print(f"\nBetween puzzles {curr_puzzle} and {next_puzzle}:")
        print(f"Difference: {hex(diff)}")
        
        # Check if difference follows a pattern
        diff_hex = hex(diff)[2:]
        print(f"Difference hex digits: {diff_hex}")
        
        # Look for patterns in the difference
        if len(diff_hex) >= 4:
            print("Notable patterns in difference:")
            for j in range(len(diff_hex)-3):
                pattern = diff_hex[j:j+4]
                if pattern.count(pattern[0]) > 1:
                    print(f"  Position {j}: {pattern}")

def predict_next_values():
    """Try to predict next values based on numeric patterns"""
    print("\nPredicting Next Values:")
    print("=" * 50)
    
    values = [(num, int(key.lstrip('0'), 16)) for num, key in known_keys]
    
    # Analyze growth pattern
    growths = []
    diffs = []
    for i in range(len(values)-1):
        curr_puzzle, curr_val = values[i]
        next_puzzle, next_val = values[i+1]
        
        growth = next_val / curr_val
        diff = next_val - curr_val
        growths.append(growth)
        diffs.append(diff)
    
    avg_growth = sum(growths) / len(growths)
    avg_diff = sum(diffs) / len(diffs)
    
    print(f"Average growth factor: {avg_growth:.4f}")
    print(f"Average difference: {hex(int(avg_diff))}")
    
    # Last known value
    last_puzzle, last_value = values[-1]
    
    # Predict next values
    for puzzle in range(67, 70):
        steps = puzzle - last_puzzle
        # Try both growth and difference predictions
        growth_pred = int(last_value * (avg_growth ** steps))
        diff_pred = int(last_value + (avg_diff * steps))
        
        print(f"\nPredictions for puzzle {puzzle}:")
        print(f"By growth: {hex(growth_pred)}")
        print(f"By diff:   {hex(diff_pred)}")

# Run analysis
analyze_numeric_pattern()
find_numeric_progression()
predict_next_values()

