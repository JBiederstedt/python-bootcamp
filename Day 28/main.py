from tkinter import *

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
REPS = 0

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global REPS

    REPS += 1

    if REPS == 8:
        label_timer.config(text="Break", fg=RED)
        count_down(LONG_BREAK_MIN * 60)
    elif REPS % 2 == 0:
        label_timer.config(text="Break", fg=PINK)
        count_down(SHORT_BREAK_MIN * 60)
    else:
        label_timer.config(text="Work", fg=GREEN)
        count_down(WORK_MIN * 60)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global REPS

    count_min = count // 60
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    
    canvas.itemconfig(clock, text=f"{count_min}:{count_sec}")

    if count > 0:
        window.after(1000, count_down, count - 1)
    else:
        if REPS % 2 == 1:  
            checks = "✔" * ((REPS // 2) + 1)
            label_checks.config(text=checks)

        if REPS == 8:
            REPS = 0

        start_timer()

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

label_checks = Label(fg=GREEN, bg=YELLOW, font=(FONT_NAME, FONT_SIZE_LABEL, FONT_STYLE_LABEL))
label_checks.grid(row=3, column=1)

btn_start = Button(text="Start", padx=10, pady=10, borderwidth=0, command=start_timer)
btn_start.grid(row=2, column=0)

btn_reset = Button(text="Reset", padx=10, pady=10, borderwidth=0)
btn_reset.grid(row=2, column=2)

window.mainloop()
