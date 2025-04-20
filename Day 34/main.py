# ---------------------------- IMPORTS ------------------------------- #

from question_model import Question
from data import get_questions
from quiz_brain import QuizBrain
from ui import QuizzInterface

# ---------------------------- ENTRY POINT ------------------------------- #

question_data = get_questions()

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = QuizBrain(question_bank)
quiz_interface = QuizzInterface(quiz)
