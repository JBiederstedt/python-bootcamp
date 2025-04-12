from turtle import Turtle

INITIAL_SCORE = 0
TEXT_COLOR = "white"
TEXT_ALIGNMENT = "center"
TEXT_FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = INITIAL_SCORE
        self.penup()
        self.hideturtle()
        self.color(TEXT_COLOR)
        self.goto(0, 270)
        self.update_scoreboard()
    
    def update_scoreboard(self):
        self.write(f"Score: {self.score}", align=TEXT_ALIGNMENT, font=TEXT_FONT)
    
    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()
    
    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=TEXT_ALIGNMENT, font=TEXT_FONT)
