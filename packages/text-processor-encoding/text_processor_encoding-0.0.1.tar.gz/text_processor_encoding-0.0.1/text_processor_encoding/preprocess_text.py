import string 

def decode_text(text):
    return ''.join(char for char in text if ord(char)<128)

def remove_punctuation(text):
    return ''.join(char if char not in string.punctuation else f'\{char}' for char in text)