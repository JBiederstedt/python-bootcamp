import turtle
import pandas

# Set up screen and background image
screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

# Load state data
file = pandas.read_csv("50_states.csv")
all_states = file.state.to_list()

# Track guessed states
guessed_states = []

while len(guessed_states) < 50:
    answer_state = screen.textinput(
        title=f"{len(guessed_states)}/50 States Correct",
        prompt="What's another state's name? (Type 'Exit' to quit)"
    )

    if answer_state is None:
        continue  # Handle dialog closed with X

    answer_state = answer_state.strip().title()

    if answer_state == "Exit":
        break

    if answer_state in guessed_states:
        print(f"You already guessed {answer_state}.")
        continue

    if answer_state in all_states:
        guessed_states.append(answer_state)
        state_data = file[file.state == answer_state]
        x = int(state_data.x.values[0])
        y = int(state_data.y.values[0])

        writer = turtle.Turtle()
        writer.hideturtle()
        writer.penup()
        writer.goto(x, y)
        writer.write(answer_state, align="center", font=("Arial", 8, "bold"))
    else:
        print(f"{answer_state} is not a valid U.S. state.")

# Save missed states to file
missed_states = [state for state in all_states if state not in guessed_states]
missed_df = pandas.DataFrame(missed_states)
missed_df.to_csv("states_to_learn.csv", index=False)

# Show different message depending on how the game ended
if len(guessed_states) == 50:
    screen.textinput(
        title="🎉 Congratulations!",
        prompt="You guessed all 50 states! Amazing job!\n\n(Click OK to close)"
    )
else:
    screen.textinput(
        title="Game Over",
        prompt="Thanks for playing! Missed states saved to 'states_to_learn.csv'.\n\n(Click OK to close)"
    )
