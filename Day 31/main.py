# ---------------------------- IMPORTS ------------------------------- #

from tkinter import *
from tkinter import messagebox
import pandas

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Arial", 40, "italic")
FONT_WORD = ("Arial", 60, "bold")
LANGUAGE_FROM = "French"
LANGUAGE_TO = "English"
TIME_TO_FLIP_CARD = 3000 # milliseconds
FILE = "data/french_words.csv"

# ---------------------------- VARIABLES ------------------------------- #

random_row = None

# ---------------------------- GET DATA ------------------------------- #

try:
    data = pandas.read_csv(FILE)
except FileNotFoundError:
    messagebox.showerror("Error", "Missing File")
    exit()

# ---------------------------- GENERATE NEXT CARD ------------------------------- #

def next_card():
    global random_row, timer

    if timer:
        window.after_cancel(timer)

    random_row = data.sample().iloc[0]

    canvas.itemconfig(card_img, image=card_front_img)
    canvas.itemconfig(card_title, text=LANGUAGE_FROM, fill="black")
    canvas.itemconfig(card_word, text=random_row[LANGUAGE_FROM], fill="black")

    timer = window.after(TIME_TO_FLIP_CARD, flip_card)

# ---------------------------- FLIP CARD ------------------------------- #

def flip_card():
    canvas.itemconfig(card_img, image=card_back_img)
    canvas.itemconfig(card_title, text=LANGUAGE_TO, fill="white")
    canvas.itemconfig(card_word, text=random_row[LANGUAGE_TO], fill="white")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(TIME_TO_FLIP_CARD, flip_card)

# Card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_img = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, font=FONT_LANGUAGE)
card_word = canvas.create_text(400, 263, font=FONT_WORD)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
btn_wrong_img = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=btn_wrong_img, highlightthickness=0, borderwidth=0, command=next_card)
btn_wrong.grid(row=1, column=0)

btn_right_img = PhotoImage(file="images/right.png")
btn_right = Button(image=btn_right_img, highlightthickness=0, borderwidth=0, command=next_card)
btn_right.grid(row=1, column=1)

next_card()

window.mainloop()
