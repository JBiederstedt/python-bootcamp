# ---------------------------- IMPORTS ------------------------------- #

from tkinter import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=60)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels

label_website = Label(text="Website:", pady=5)
label_website.grid(row=1, column=0)

label_email = Label(text="Email/Username:", pady=5)
label_email.grid(row=2, column=0)

label_password = Label(text="Password:", pady=5)
label_password.grid(row=3, column=0)

# Entries

entry_website = Entry(width=37)
entry_website.grid(row=1, column=1, columnspan=2)

entry_email = Entry(width=37)
entry_email.grid(row=2, column=1, columnspan=2)

entry_password = Entry(width=21)
entry_password.grid(row=3, column=1)

# Buttons

btn_generate_password = Button(text="Generate Password", width=12)
btn_generate_password.grid(row=3, column=2)

btn_add_password = Button(text="Add Password", width=35)
btn_add_password.grid(row=4, column=1, columnspan=2)

window.mainloop()
