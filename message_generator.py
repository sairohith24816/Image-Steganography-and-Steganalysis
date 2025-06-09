import lorem

def generate_message_by_words(word_count):

    # Generate an English sentence with specified number of words using Lorem Ipsum

    if word_count <= 0:
        return ""

    text = lorem.text()
    words = text.split()

    while len(words) < word_count:
        words += lorem.text().split()

    sentence = ' '.join(words[:word_count])
    sentence = sentence[0].upper() + sentence[1:]  # Capitalize first letter
    if not sentence.endswith('.'):
        sentence += '.'

    return sentence

def generate_message_by_length(length):
    # Generate an English message with specified character length using Lorem Ipsum

    if length <= 0:
        return ""
    
    text = lorem.text()
    while len(text) < length:
        text += " " + lorem.text()
    
    if len(text) <= length:
        message = text
    else:
        # Try to cut at a word boundary
        truncated = text[:length]
        last_space = truncated.rfind(' ')
        
        if last_space > length * 0.8:  # If we can cut at a word boundary without losing too much
            message = truncated[:last_space]
        else:
            message = truncated
    
    message = message.strip()
    if message:
        message = message[0].upper() + message[1:]
        if not message.endswith('.'):
            message += '.'
    
    return message



# print(generate_message_by_words(10))  # Example usage
# print(generate_message_by_length(100))  # Example usage




if __name__ == "__main__":
    print(f'message of 5 words: {generate_message_by_words(5)}')
    print(f'message of 50 characters: {generate_message_by_length(50)}')