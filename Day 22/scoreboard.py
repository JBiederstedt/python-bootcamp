from turtle import Turtle

SCORE_COLOR = "white"
SCORE_FONT = ("Courier", 32, "normal")
SCORE_POSITION = (0, 250)
INITIAL_SCORE_P_L = 0
INITIAL_SCORE_P_R = 0

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color(SCORE_COLOR)
        self.score_paddle_left = INITIAL_SCORE_P_L
        self.score_paddle_right = INITIAL_SCORE_P_R
        self.goto(SCORE_POSITION)
        self.update_score()
    
    def update_score(self, paddle = ""):
        self.clear()
        if paddle == "left":
            self.score_paddle_left += 1
        if paddle == "right":
            self.score_paddle_right += 1

        self.write(f"{int(self.score_paddle_left)} : {int(self.score_paddle_right)}",align="center", font=SCORE_FONT)
    
    def show_winner(self, winner):
        self.goto(0, 0)
        if winner == "left":
            self.write(f"Player left won with {int(self.score_paddle_left)} : {int(self.score_paddle_right)}", align="center", font=SCORE_FONT)
        if winner == "right":
            self.write(f"Player right won with {int(self.score_paddle_left)} : {int(self.score_paddle_right)}", align="center", font=SCORE_FONT)
