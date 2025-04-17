from tkinter import *

def btn_clicked():
    if entry.get() == "" or entry.get() == "0":
        label_to_km["text"] = 0
    else:
        label_to_km["text"] = round(float(entry.get()) * 1.609, 2)

window = Tk()
window.minsize(width=400, height=200)
window.title("Miles to Km Converter")
window.config(padx=75, pady=70)

label_is_equal_to = Label(text="is equal to")
label_is_equal_to.grid(row=1, column=0)

entry = Entry(width=10, justify="center")
entry.insert(0, "0")
entry.grid(row=0, column=1)
entry.focus()

label_to_km = Label(text=0, font=("arial", 16, "bold"))
label_to_km.grid(row=1, column=1)
label_to_km.config(padx=20, pady=20)

button = Button(text="Calculate", command=btn_clicked)
button.grid(row=2, column=1)

label_miles = Label(text="Miles")
label_miles.grid(row=0, column=2)

label_km = Label(text="Km")
label_km.grid(row=1, column=2)

window.mainloop()
