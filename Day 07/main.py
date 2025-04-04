import random
from hangman_art import stages, logo
from hangman_words import word_list

print(logo)

chosen_word = random.choice(word_list)
word_length = len(chosen_word)
lives = len(stages) - 1
game_is_finished = False

display = ["_" for _ in range(word_length)]

print("\n" + ' '.join(display) + "\n")

while not game_is_finished:
    guess = input("Guess a letter: ").lower()
    print()

    if guess in display:
        print(f"You've already guessed {guess}\n")

    for position in range(word_length):
        letter = chosen_word[position]
        if letter == guess:
            display[position] = letter

    print(' '.join(display) + "\n")

    if guess not in chosen_word:
        print(f"You guessed {guess}, that's not in the word. You lose a life.\n")
        lives -= 1
        if lives == 0:
            game_is_finished = True
            print("You lose.\n")

    if "_" not in display:
        game_is_finished = True
        print("You win.\n")

    print(stages[lives])
