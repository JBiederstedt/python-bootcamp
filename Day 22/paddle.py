from turtle import Turtle

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_COLOR = "white"
PADDLE_SHAPE = "square"

class Paddle(Turtle):
    def __init__(self, paddle_cor):
        super().__init__()
        self.shape(PADDLE_SHAPE)
        self.color(PADDLE_COLOR)
        self.shapesize(PADDLE_HEIGHT / 20, PADDLE_WIDTH / 20)
        self.penup()
        self.goto(paddle_cor)
    
    def move_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def move_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)
