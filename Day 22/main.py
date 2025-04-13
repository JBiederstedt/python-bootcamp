from turtle import Screen
import time
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Pong Game")
screen.tracer(0)

paddle_left = Paddle((-360, 0))
paddle_right = Paddle((350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(key="w", fun=paddle_left.move_up)
screen.onkey(key="s", fun=paddle_left.move_down)
screen.onkey(key="Up", fun=paddle_right.move_up)
screen.onkey(key="Down", fun=paddle_right.move_down)

game_is_on = True
while game_is_on:
    time.sleep(ball.ball_speed)
    screen.update()
    ball.move()

    # Detect collision with wall
    if ball.ycor() > 280 or ball.ycor() < -270:
        ball.bounce_y()

    # Detect collision with paddle
    if ball.distance(paddle_right) < 50 and ball.xcor() > 320 or ball.distance(paddle_left) < 40 and ball.xcor() < -330:
        ball.bounce_x()
    
    # Detect when right paddle missed
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.update_score("left")
    
    # Detect when left paddle missed
    if ball.xcor() < -390:
        ball.reset_position()
        scoreboard.update_score("right")
    
    # End game when one player has a score of 5
    if scoreboard.score_paddle_left == 5:
        game_is_on = False
        scoreboard.show_winner("left")
    if scoreboard.score_paddle_right == 5:
        game_is_on = False
        scoreboard.show_winner("right")

screen.exitonclick()
