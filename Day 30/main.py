# ---------------------------- IMPORTS ------------------------------- #

from tkinter import *
from tkinter import messagebox
import pyperclip
import json
from password_generator import password_generator

# ---------------------------- CONSTANTS ------------------------------- #

CREDENTIALS_FILE = "credentials.json"
DEFAULT_EMAIL   = "placeholder@email.com"

# ---------------------------- GENERATE PASSWORD ------------------------------- #

def generate_password():
    password = password_generator()

    # Update password entry
    entry_password.delete(0, END)
    entry_password.insert(0, password)

    # Copy password to clipboard
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def add_credentials():
    global CREDENTIALS_FILE, DEFAULT_EMAIL

    website = entry_website.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()
    new_credentials = {
        website: {
            "email/username": email,
            "password": password,
        }
    }

    empty_entries = not website or not email or not password

    if empty_entries:
        message_missing_entries = "Missing Entries"
        messagebox.showwarning(title="Empty Entries", message=message_missing_entries)

        return

    message_save = f"""\
                Do you want to save these credentials?

                Website: {website}
                Email/Username: {email}
                Password: {password}

                Press OK to save."""
    user_confirmation = messagebox.askokcancel(title=website, message=message_save)

    if user_confirmation:
        try:
            with open(CREDENTIALS_FILE, mode="r") as credentials_file:
                data = json.load(credentials_file)
                data.update(new_credentials)
        except FileNotFoundError:
            with open(CREDENTIALS_FILE, mode="w") as credentials_file:
                json.dump(new_credentials, credentials_file, indent=4)
        else:
            with open(CREDENTIALS_FILE, mode="w") as credentials_file:
                json.dump(data, credentials_file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_email.delete(0, END)
            entry_email.insert(0, DEFAULT_EMAIL)
            entry_password.delete(0, END)

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
entry_website.focus()

entry_email = Entry(width=37)
entry_email.grid(row=2, column=1, columnspan=2)
entry_email.insert(0, DEFAULT_EMAIL)

entry_password = Entry(width=21)
entry_password.grid(row=3, column=1)

# Buttons
btn_generate_password = Button(text="Generate Password", width=12, command=generate_password)
btn_generate_password.grid(row=3, column=2)

btn_add_credentials = Button(text="Add Credentials", width=35, command=add_credentials)
btn_add_credentials.grid(row=4, column=1, columnspan=2)

window.mainloop()
