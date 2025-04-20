# ---------------------------- IMPORTS ------------------------------- #

from tkinter import *
from quiz_brain import QuizBrain

# ---------------------------- CONSTANTS ------------------------------- #

THEME_COLOR = "#375362"
FONT_SCORE = ("arial", 16)
FONT_QUESTION = ("arial", 20, "italic")
FILE_PATH_BTN_TRUE_IMG = "images/true.png"
FILE_PATH_BTN_FALSE_IMG = "images/false.png"

# ---------------------------- CLASS DEF ------------------------------- #

class QuizzInterface:

    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        self.window = Tk()
        self.window.title("Quiz App")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # Score label
        self.label_score = Label(text="Score: 0", bg=THEME_COLOR, fg="white", font=FONT_SCORE)
        self.label_score.grid(row=0, column=1)

        # Question card
        self.canvas = Canvas(width=300, height=250, bg="white")
        self.question = self.canvas.create_text(150, 125,
                                                width=280,
                                                text="Loading question...",
                                                font=FONT_QUESTION,
                                                fill=THEME_COLOR,
                                                anchor="center",
                                                justify="center")
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # Buttons
        btn_true_img = PhotoImage(file=FILE_PATH_BTN_TRUE_IMG)
        self.btn_true = Button(image=btn_true_img, highlightthickness=0, borderwidth=0, command=self.true_clicked)
        self.btn_true.grid(row=2, column=0)

        btn_false_img = PhotoImage(file=FILE_PATH_BTN_FALSE_IMG)
        self.btn_false = Button(image=btn_false_img, highlightthickness=0, borderwidth=0, command=self.false_clicked)
        self.btn_false.grid(row=2, column=1)

        self.next_question()

        self.window.mainloop()

    def next_question(self):
        self.canvas.config(bg="white")
        self.label_score.config(text=f"Score: {self.quiz.score}")

        if self.quiz.still_has_questions():
            question_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question, text=question_text)
        else:
            text = f"""\
You've completed the quiz.

Your final score was: {self.quiz.score}/{self.quiz.question_number}
"""
            self.canvas.itemconfig(self.question, text=text)
            self.canvas.config(bg="lightblue")
            self.btn_true.config(state="disabled")
            self.btn_false.config(state="disabled")

    def true_clicked(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_clicked(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, user_is_right):
        if user_is_right:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, self.next_question)
