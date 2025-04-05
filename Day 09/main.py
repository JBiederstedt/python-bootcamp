import art

print(art.logo)
print()

auction = {}
stop_auction = False
question = "yes"

while not stop_auction:
    if question == "yes":
        key = input("What is your name?: ").title()
        print()
        value = int(input("What is your bid?: $"))
        print()
        auction[key] = value
        question = input("Are there any other bidders? Type 'yes' or 'no'. ").lower()
        print()
        if question == "yes":
            print("\n" * 20)
    elif question == "no":
        stop_auction = True
    else:
        print("You've picked an invalid keyword.\nEnd of the auction.")
        stop_auction = True

winner = max(auction, key=auction.get)
amount = auction[winner]

print(f"The winner is {winner} with a bid of ${amount}.")
print()
