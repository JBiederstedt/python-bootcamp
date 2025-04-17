import pandas

# TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}

file = pandas.read_csv("nato_phonetic_alphabet.csv")

phonetic_dict = {row.letter:row.code for (_, row) in file.iterrows()}

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.
word = input("What word would you like in NATO Alphabet?\n> ").upper()

code_words_list = [phonetic_dict[letter] for letter in word if not letter == " "]

print(f"> {code_words_list}")
