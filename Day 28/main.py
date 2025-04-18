from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
FONT_COLOR_CLOCK = "white"
FONT_SIZE_CLOCK = 35
FONT_SIZE_LABEL = 50
FONT_STYLE_CLOCK = "bold"
FONT_STYLE_LABEL = "normal"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    count_down(WORK_MIN * 60)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    canvas.itemconfig(clock, text=f"{count_min}:{count_sec}")
    if count > 0:
        window.after(1000, count_down, count - 1)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
clock = canvas.create_text(100, 130, text="00:00", fill=FONT_COLOR_CLOCK, font=(FONT_NAME, FONT_SIZE_CLOCK, FONT_STYLE_CLOCK))
canvas.grid(row=1, column=1)

label_timer = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, FONT_SIZE_LABEL, FONT_STYLE_LABEL), pady=10)
label_timer.grid(row=0, column=1)

label_check = Label(text="✔", fg=GREEN, bg=YELLOW, font=(FONT_NAME, FONT_SIZE_LABEL, FONT_STYLE_LABEL))
label_check.grid(row=3, column=1)

btn_start = Button(text="Start", padx=10, pady=10, borderwidth=0, command=start_timer)
btn_start.grid(row=2, column=0)

btn_reset = Button(text="Reset", padx=10, pady=10, borderwidth=0)
btn_reset.grid(row=2, column=2)

window.mainloop()
