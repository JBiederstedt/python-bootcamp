import art

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

print(art.logo)
print()

def ceasar(direction_parameter, text_parameter, shift_parameter):
    cipher_text = ""

    for n in text_parameter:
        if n in alphabet:
            text_position = alphabet.index(n)

            if direction_parameter == "encode":
                new_position = text_position + shift_parameter
                new_position = new_position % 26

            elif direction_parameter == "decode":
                new_position = text_position - shift_parameter
                new_position = new_position % 26
                    
            new_letter = alphabet[new_position]
            cipher_text += new_letter
        else:
            cipher_text += n
            
    print(f"Here's the {direction_parameter}d result: {cipher_text}")
    print()

cipher_end = False
while not cipher_end:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
    print()

    if direction == "encode" or direction == "decode":
        text = input("Type your message:\n").lower()
        print()
        shift = int(input("Type the shift number:\n"))
        print()
    else:
        print("Please pick a valid keyword.\n")
        break

    if direction == "encode" or direction == "decode":
        ceasar(direction_parameter=direction, text_parameter=text, shift_parameter=shift)

    cipher_command = input("Type 'yes' if you want to go again. Otherwise type 'no':\n")
    print()
    if cipher_command == "yes":
        cipher_end = False
    elif cipher_command == "no":
        cipher_end = True
        print("Goodbye!\n")
    else:
        print("Please pick a valid keyword.\n")
        break
