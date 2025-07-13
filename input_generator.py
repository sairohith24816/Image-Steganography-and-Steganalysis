import random
import message_generator

def generate_steganography_input(rows=256, columns=256):
    
    start_row = random.randint(0, int(rows * 0.50))
    start_col = random.randint(0, int(columns * 0.50))
    start_position = (start_row, start_col)
    
    num_bits = random.randint(1, 8)
    
    channels_options = ['R', 'G', 'B', 'RG', 'RB', 'GB', 'RGB']
    channels = random.choice(channels_options)
    
    gap = random.randint(0, 5)
    
    horizontal = random.choice([0, 1])
    
    delimiter_options = [
        ('#', '#'),           
        ('##', '##'),         
        ('***', '***'),      
        ('[START]', '[END]'), 
        ('<START>', '<END>'),
        ('<<START>>', '<<END>>'),
        ('<<', '>>'),         
        ('{', '}'),          
        ('|', '|'),        
        ('+++', '+++'),    
        ('BEGIN', 'END'), 
        ('---', '---'),     
        ('!!!', '!!!'),  
        ('$$$', '$$$'),    
        ('&&&', '&&&'),  
        ('@@', '@@'),        ]
    delimiter_start, delimiter_end = random.choice(delimiter_options)
    
    # Calculate max message length using SAME logic as encode_message function
    bits_per_pixel = len(channels) * num_bits
    
    # Use IDENTICAL capacity calculation as in encode_message function
    if horizontal:
        # Row-wise: remaining pixels in current row + all pixels in remaining rows
        total_pixels = (columns - start_col) + (rows - start_row - 1) * columns
    else:
        # Column-wise: remaining pixels in current column + all pixels in remaining columns  
        total_pixels = (rows - start_row) + (columns - start_col - 1) * rows
    
    # Account for gap: every (gap+1) pixels, we can use 1 pixel
    available_pixels = total_pixels // (gap + 1)
    available_bits = available_pixels * bits_per_pixel
    
    # CRITICAL: Account for delimiter bits
    delimiter_bits = (len(delimiter_start) + len(delimiter_end)) * 8
    message_bits = available_bits - delimiter_bits
    
    # NEW: Account for potential bit padding in encoder (add 7 bits safety margin)
    # This handles cases where the encoder might need to pad incomplete bytes
    padding_safety_bits = 7
    message_bits -= padding_safety_bits
    
    # Ensure we have enough bits for at least 1 character
    if message_bits < 8:
        message_bits = 0
    
    max_characters = message_bits // 8
    
    if max_characters < 1:
        raise ValueError("!!! Cannot encode any message with the given constraints.")

    # Generate message with 10-20% of max capacity (reduced from 25% for more safety)
    # Add additional safety buffer to avoid edge cases
    safe_max_characters = max(1, max_characters - 3)  # Increased safety buffer from 2 to 3
    
    # Ensure safe_max_characters is positive
    if safe_max_characters < 1:
        safe_max_characters = 1
    
    # Use more conservative percentage range
    min_length = max(1, int(safe_max_characters * 0.60))
    max_length = max(min_length, int(safe_max_characters * 0.90))  # Reduced from 0.25
    
    message_length = random.randint(min_length, max_length)
    message = message_generator.generate_message_by_length(message_length)
    actual_message_length = len(message)
    
    # VALIDATION: Double-check our calculation
    required_bits = (actual_message_length * 8) + delimiter_bits + padding_safety_bits
    if required_bits > available_bits:
        # Fallback: generate smaller message
        fallback_max_chars = max(1, (available_bits - delimiter_bits - padding_safety_bits) // 8 - 1)
        message = message_generator.generate_message_by_length(fallback_max_chars)
        actual_message_length = len(message)
    
    return {
        'start_position': start_position,
        'channels': channels,
        'gap': gap,
        'horizontal': horizontal,
        'num_bits': num_bits,
        'message': message,
        'message_length': actual_message_length,
        'max_possible_length': max_characters,
        'utilization_percent': round((actual_message_length / max_characters) * 100, 2),
        'delimiter_start': delimiter_start,
        'delimiter_end': delimiter_end
    }

if __name__ == "__main__":
    input_data = generate_steganography_input()
    print("Steganography Input Data:")
    # for key, value in input_data.items():
    #     print(f"{key}: {value}")
    #     print()
    print(input_data['message_length'])
    print(input_data['max_possible_length'])
    print(input_data['utilization_percent'])
    print(input_data['message'])

