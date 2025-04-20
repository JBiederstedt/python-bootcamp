# ---------------------------- IMPORTS ------------------------------- #

import requests
import html

# ---------------------------- CONSTANTS ------------------------------- #

NUMBER_OF_QUESTIONS = 10
DIFFICULTY_LEVEL_EASY = "easy"
DIFFICULTY_LEVEL_MEDIUM = "medium"
DIFFICULTY_LEVEL_HARD = "hard"
API_QUIZ = f"https://opentdb.com/api.php?amount={NUMBER_OF_QUESTIONS}&difficulty={DIFFICULTY_LEVEL_MEDIUM}&type=boolean"

# ---------------------------- GET QUESTION DATA ------------------------------- #

def get_questions():
    try:
        response = requests.get(API_QUIZ)
        response.raise_for_status()

        data = response.json()
        if not data["results"]:
            print("No questions returned from API.")
            return []

        question_data = [
            {
                "question": html.unescape(result["question"]), # get rid of html entities
                "correct_answer": result["correct_answer"],
            }
            for result in data["results"]
        ]

        return question_data

    except Exception as e:
        print(f"Something went wrong:\n{e}")
        return []
