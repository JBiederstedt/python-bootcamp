# ---------------------------- IMPORTS ------------------------------- #

import random

# ---------------------------- CONSTANTS ------------------------------- #

LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "!#$%&()*+"
NUMBERS = "0123456789"

# ---------------------------- PASSWORD GENERATOR FUNCTION ------------------------------- #

def password_generator():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password = []
    password += random.choices(LETTERS, k=nr_letters)
    password += random.choices(SYMBOLS, k=nr_symbols)
    password += random.choices(NUMBERS, k=nr_numbers)

    random.shuffle(password)

    # Return password as string
    return "".join(password)
