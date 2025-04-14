PLACEHOLDER = "[name]"

with open("Input/Letters/starting_letter.txt") as starting_letter:
    letter_content = starting_letter.read()

with open("Input/Names/invited_names.txt") as invited_names:
    names = invited_names.read().splitlines()
    for name in names:
        new_letter = letter_content.replace(PLACEHOLDER, name)
        with open(f"Output/ReadyToSend/letter_for_{name}.docx", mode="w") as writer:
            writer.write(new_letter)
