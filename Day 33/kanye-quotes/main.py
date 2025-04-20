# ---------------------------- IMPORTS ------------------------------- #

from tkinter import *
import requests

# ---------------------------- CONSTANTS ------------------------------- #

API_PATH = "https://api.kanye.rest/"

# ---------------------------- GET QUOTE ------------------------------- #

def get_quote():
    try:
        response = requests.get(API_PATH, timeout=5)
        response.raise_for_status()

        data = response.json()
        quote = data["quote"]
        
        canvas.itemconfig(quote_text, text=quote)
    except Exception as e:
        canvas.itemconfig(quote_text, text="Oops! Could not fetch quote.")
        print(f"Something went wrong:\n{e}")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Kanye Says...")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=300, height=414)
background_img = PhotoImage(file="background.png")
canvas.create_image(150, 207, image=background_img)
quote_text = canvas.create_text(150, 207, width=250, font=("Arial", 30, "bold"), fill="white")
canvas.grid(row=0, column=0)

# Button
kanye_img = PhotoImage(file="kanye.png")
kanye_button = Button(image=kanye_img, highlightthickness=0, command=get_quote)
kanye_button.grid(row=1, column=0)

get_quote()

window.mainloop()
