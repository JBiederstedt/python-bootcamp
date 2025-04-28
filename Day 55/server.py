import random
from flask import Flask

# Create a new Flask web application
app = Flask(__name__)

# Generate a random number between 0 and 9 at server start
# This number remains the same until you restart the app
random_number = random.randint(0, 9)

# Home route: asks the user to guess a number and shows a gif
@app.route("/")
def home():
    # Return an HTML page with an <h1> and an image
    return """
    <h1 style="color: navy;">Guess a number between 0 and 9</h1>
    <img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" alt="Guessing gif">
    """

# Route for handling the user's guess, e.g. /3 or /7
@app.route("/<int:guess>")
def guess_number(guess):
    # If guess is too low
    if guess < random_number:
        return """
        <h1 style="color: red;">Too low! Try again.</h1>
        <img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" alt="Too low">
        """
    # If guess is too high
    elif guess > random_number:
        return """
        <h1 style="color: purple;">Too high! Try again.</h1>
        <img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" alt="Too high">
        """
    # If guess is correct
    else:
        return """
        <h1 style="color: green;">You found me! 🎉</h1>
        <img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" alt="Correct">
        """

# Entry point: start the Flask development server on port 5000
if __name__ == "__main__":
    # debug=True enables hot reload on code changes
    app.run(debug=True)
