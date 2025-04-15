import random
import game_data
import art

# Simulated screen clear
def clear():
    print("\n" * 20)

print(art.logo)
game_over = False
score = 0
list_of_index = list(range(0, len(game_data.data)))
compare_A_number = random.choice(list_of_index)

while not game_over:

    # Ensure A and B are not the same
    compare_B_list = [n for n in list_of_index if n != compare_A_number]
    compare_B_number = random.choice(compare_B_list)

    # Functions to access data
    def compare_A(key):
        return game_data.data[compare_A_number][key]

    def compare_B(key):
        return game_data.data[compare_B_number][key]

    def comparison():
        if compare_A('follower_count') > compare_B('follower_count'):
            return "a"
        elif compare_A('follower_count') < compare_B('follower_count'):
            return "b"

    # Text output setup
    Compare_A = f"{compare_A('name')}, a {compare_A('description')}, from {compare_A('country')}."
    Compare_B = f"{compare_B('name')}, a {compare_B('description')}, from {compare_B('country')}."

    # Display current round
    print(f"Compare A: {Compare_A}")
    print(art.vs)
    print(f"Against B: {Compare_B}")
    print()
    compare_input = input("Who has more followers? Type 'A' or 'B': ").lower()

    # Round result
    correct_answer = comparison()

    if compare_input == correct_answer:
        score += 1
        clear()
        print(art.logo)
        print(f"You're right! Current score: {score}.")
        print()

        # Only promote the winner to position A
        if correct_answer == "a":
            # A stays the same
            pass
        else:
            # B becomes new A
            compare_A_number = compare_B_number

    else:
        clear()
        print(art.logo)
        print(f"Sorry, that's wrong. Final score: {score}")
        print()
        game_over = True
