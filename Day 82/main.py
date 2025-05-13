# Morse code mapping for letters, digits, and some punctuation
MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.',
    '-': '-....-', '(': '-.--.',  ')': '-.--.-', ' ': '/'
}

def text_to_morse(text: str) -> str:
    """
    Convert a text string to Morse code.
    Characters without a Morse equivalent are ignored.
    """
    morse_chars = []
    for char in text.upper():
        code = MORSE_CODE_DICT.get(char)
        if code:
            morse_chars.append(code)
        # skip characters that have no mapping
    # join Morse symbols with spaces
    return ' '.join(morse_chars)

def main():
    user_input = input("\nEnter text to convert to Morse code: ")
    morse_output = text_to_morse(user_input)
    print("\nMorse Code Output:\n" + morse_output)
    print()

if __name__ == "__main__":
    main()
