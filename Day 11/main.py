import random
import art

def draw_card(count):
    """Returns a LIST with 'count' amount of random cards."""
    card_deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return [random.choice(card_deck) for _ in range(count)]

def calculate_score(card_list):
    """Returns the sum of card values as INT, 0 meaning a Blackjack."""
    temp_card_list = card_list.copy()
    temp_card_list.sort(reverse=True)

    if temp_card_list == [11, 10]:
        return 0

    score = sum(temp_card_list)
    while score > 21 and 11 in temp_card_list:
        temp_card_list[temp_card_list.index(11)] = 1
        score = sum(temp_card_list)

    return score

def display_score(players, game_over):
    """Display the score for dealer and player."""
    dealer = players[0]
    user = players[1]

    if dealer["has_blackjack"]:
        print(f"Dealer's cards: {fix_aces(dealer['cards'])} BLACKJACK!")
    elif game_over:
        print(f"Dealer's cards: {fix_aces(dealer['cards'])} Score: {dealer['score']}")
    else:
        print(f"Dealer's first card: {fix_aces(dealer['revealed_cards'])} Score: ??")

    if user["has_blackjack"]:
        print(f"Your cards: {fix_aces(user['cards'])} BLACKJACK!")
    else:
        print(f"Your cards: {fix_aces(user['cards'])} Score: {user['score']}")

def fix_aces(card_list):
    """Formats card list as string, converting 11 to [A]."""
    return "".join([f"[A]" if val == 11 else f"[{val}]" for val in card_list])

def play():
    """Play one round of the game."""
    cpu = {"cards": [], "revealed_cards": [], "score": 0, "has_blackjack": False}
    user = {"cards": [], "score": 0, "has_blackjack": False}
    players = [cpu, user]

    is_game_over = False

    for player in players:
        player["cards"] = draw_card(2)
        player["score"] = calculate_score(player["cards"])
        player["has_blackjack"] = player["score"] == 0

    cpu["revealed_cards"] = [cpu["cards"][0]]

    if cpu["has_blackjack"] or user["has_blackjack"]:
        is_game_over = True

    # User turn
    if not is_game_over:
        while True:
            display_score(players, is_game_over)
            choice = input('\nType "y" to get another card, type "n" to pass.\n> ')
            print()
            if choice.lower() == "y":
                print("You draw a card.\n")
                user["cards"].extend(draw_card(1))
                user["score"] = calculate_score(user["cards"])
                if user["score"] > 21:
                    is_game_over = True
                    break
            else:
                break

    # Dealer turn
    if not is_game_over:
        while cpu["score"] < 17:
            print("The dealer draws a card.\n")
            cpu["cards"].extend(draw_card(1))
            cpu["score"] = calculate_score(cpu["cards"])

    is_game_over = True
    display_score(players, is_game_over)

    # Result
    if cpu["has_blackjack"] and not user["has_blackjack"]:
        print("\nDealer has a blackjack, DEALER wins.\n")
    elif cpu["has_blackjack"] and user["has_blackjack"]:
        print("\nYou both have a blackjack, it's a tie!\n")
    elif user["has_blackjack"]:
        print("\nYou have a blackjack, YOU win.\n")
    elif cpu["score"] > 21:
        print("\nDealer went over. YOU win.\n")
    elif user["score"] > 21:
        print("\nYou went over. DEALER wins.\n")
    elif user["score"] == cpu["score"]:
        print("\nIt's a tie!\n")
    elif user["score"] > cpu["score"]:
        print("\nYOU win.\n")
    else:
        print("\nDEALER wins.\n")

while True:
    print(art.logo)
    play()
    again = input("Do you want to play another round? (y/n)\n> ")
    print()
    if again.lower() != "y":
        break
    print("\n" * 20)

print("Thanks for playing!")
print()
