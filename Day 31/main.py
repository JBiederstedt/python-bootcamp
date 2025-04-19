# ---------------------------- IMPORTS ------------------------------- #

from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Arial", 40, "italic")
FONT_WORD = ("Arial", 60, "bold")
LANGUAGE_FROM = "French"

WORD = "test"

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
canvas.create_image(400, 263, image=card_front_img, anchor="center")
language_from = canvas.create_text(400, 150, text=LANGUAGE_FROM, font=FONT_LANGUAGE)
word_from = canvas.create_text(400, 263, text=WORD, font=FONT_WORD)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
btn_wrong_img = PhotoImage(file="images/wrong.png")
btn_wrong = Button(image=btn_wrong_img, highlightthickness=0, borderwidth=0,
                   bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)
btn_wrong.grid(row=1, column=0)

btn_right_img = PhotoImage(file="images/right.png")
btn_right = Button(image=btn_right_img, highlightthickness=0, borderwidth=0,
                   bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)
btn_right.grid(row=1, column=1)

window.mainloop()
