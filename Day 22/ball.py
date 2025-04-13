from turtle import Turtle

BALL_COLOR = "white"
BALL_SHAPE = "circle"
INITIAL_BALL_SPEED = 0.1
MAX_BALL_SPEED = 0.05
X_MOVE = 10
Y_MOVE = 10

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color(BALL_COLOR)
        self.shape(BALL_SHAPE)
        self.penup()
        self.x_move = X_MOVE
        self.y_move = Y_MOVE
        self.ball_speed = INITIAL_BALL_SPEED
    
    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)
    
    def bounce_y(self):
        self.y_move *= -1
    
    def bounce_x(self):
        self.x_move *= -1
        self.ball_speed *= 0.9
        if self.ball_speed < MAX_BALL_SPEED:
            self.ball_speed = MAX_BALL_SPEED

    def reset_position(self):
        self.goto(0, 0)
        self.ball_speed = INITIAL_BALL_SPEED
        self.x_move *= -1
