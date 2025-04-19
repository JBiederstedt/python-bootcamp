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
FILE_COMPLETE = "data/french_words.csv"
FILE_WORDS_REMAINING = "data/words_remaining.csv"
FILE_WORDS_TO_LEARN = "data/words_to_learn.csv"

# ---------------------------- VARIABLES ------------------------------- #

random_row = None
timer = None

# ---------------------------- GET DATA ------------------------------- #

try:
    data = pandas.read_csv(FILE_WORDS_REMAINING)
except FileNotFoundError:
    try:
        data = pandas.read_csv(FILE_COMPLETE)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Missing File.")
        exit()

# ---------------------------- GENERATE NEXT CARD ------------------------------- #

def next_card():
    global random_row, timer

    if data.empty:
        messagebox.showinfo(title="Congratulations!", message="You've learned all available words 🎉")
        window.quit()

        return

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

# ---------------------------- DELETE KNOWN WORD ------------------------------- #

def delete_known_word():
    global data
    
    data = data.drop(random_row.name)

# ---------------------------- WRITE WORD TO LEARN ------------------------------- #

def write_word_to_learn():
    df_to_learn = pandas.DataFrame([random_row])

    try:
        df_existing = pandas.read_csv(FILE_WORDS_TO_LEARN)

        if not df_existing[
            (df_existing[LANGUAGE_FROM] == random_row[LANGUAGE_FROM]) &
            (df_existing[LANGUAGE_TO] == random_row[LANGUAGE_TO])
        ].empty:
            return

        df_to_learn = pandas.concat([df_existing, df_to_learn], ignore_index=True)
    except FileNotFoundError:
        pass

    df_to_learn.to_csv(FILE_WORDS_TO_LEARN, index=False)

# ---------------------------- RIGHT ANSWER ------------------------------- #

def right_answer():
    delete_known_word()
    next_card()

# ---------------------------- WRONG ANSWER ------------------------------- #

def wrong_answer():
    write_word_to_learn()
    next_card()

# ---------------------------- SAVE PROGRESS ------------------------------- #

def save_progress():
    data.to_csv(FILE_WORDS_REMAINING, index=False)

# ---------------------------- ON CLOSING ------------------------------- #

def on_closing():
    save_progress()
    window.destroy()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

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
btn_wrong = Button(image=btn_wrong_img, highlightthickness=0, borderwidth=0, command=wrong_answer)
btn_wrong.grid(row=1, column=0)

btn_right_img = PhotoImage(file="images/right.png")
btn_right = Button(image=btn_right_img, highlightthickness=0, borderwidth=0, command=right_answer)
btn_right.grid(row=1, column=1)

next_card()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
