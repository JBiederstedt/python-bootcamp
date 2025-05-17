# breakout_game.py

from turtle import Screen, Turtle
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_ROWS = 5
BRICKS_PER_ROW = 8
BRICK_WIDTH = 4   # turtle units (1 unit = 20 pixels)
BRICK_HEIGHT = 1
BRICK_PADDING = 10  # pixels
BRICK_START_Y = 250
PADDLE_MOVE_DISTANCE = 20
PADDLE_HALF_WIDTH = 50  # pixels (stretch_len * 20 / 2)

class Paddle(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.color('white')
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.goto(0, -SCREEN_HEIGHT/2 + 50)

    def move_left(self):
        new_x = self.xcor() - PADDLE_MOVE_DISTANCE
        min_x = -SCREEN_WIDTH/2 + PADDLE_HALF_WIDTH
        if new_x < min_x:
            new_x = min_x
        self.goto(new_x, self.ycor())

    def move_right(self):
        new_x = self.xcor() + PADDLE_MOVE_DISTANCE
        max_x = SCREEN_WIDTH/2 - PADDLE_HALF_WIDTH
        if new_x > max_x:
            new_x = max_x
        self.goto(new_x, self.ycor())

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('white')
        self.penup()
        self.dx = 4
        self.dy = 4

    def move(self):
        self.goto(self.xcor() + self.dx, self.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1

    def reset_position(self):
        self.goto(0, 0)
        self.bounce_y()

class Brick(Turtle):
    def __init__(self, position, color):
        super().__init__()
        self.shape('square')
        self.color(color)
        self.shapesize(stretch_wid=BRICK_HEIGHT, stretch_len=BRICK_WIDTH)
        self.penup()
        self.goto(position)

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color('white')
        self.penup()
        self.hideturtle()
        self.goto(-SCREEN_WIDTH/2 + 20, SCREEN_HEIGHT/2 - 40)
        self.update_score()

    def update_score(self):
        self.clear()
        self.write(f'Score: {self.score}', align='left', font=('Arial', 16, 'normal'))

    def increase_score(self):
        self.score += 1
        self.update_score()

    def game_over(self):
        self.goto(0, 0)
        self.write('GAME OVER', align='center', font=('Arial', 24, 'bold'))

    def win(self):
        self.goto(0, 0)
        self.write('YOU WIN!', align='center', font=('Arial', 24, 'bold'))


def create_bricks():
    bricks = []
    colors = ['red', 'orange', 'yellow', 'green', 'blue']
    y = BRICK_START_Y
    for row in range(BRICK_ROWS):
        x_start = - (BRICKS_PER_ROW * BRICK_WIDTH * 20) / 2 + (BRICK_WIDTH * 20) / 2
        for col in range(BRICKS_PER_ROW):
            x = x_start + col * (BRICK_WIDTH * 20 + BRICK_PADDING)
            brick = Brick((x, y), colors[row % len(colors)])
            bricks.append(brick)
        y -= (BRICK_HEIGHT * 20 + BRICK_PADDING)
    return bricks


def main():
    screen = Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.bgcolor('black')
    screen.title('Breakout')
    screen.tracer(0)

    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    scoreboard = Scoreboard()

    screen.listen()
    screen.onkey(paddle.move_left, 'Left')
    screen.onkey(paddle.move_right, 'Right')

    game_is_on = True
    while game_is_on:
        time.sleep(0.017)
        screen.update()
        ball.move()

        # Detect collision with walls
        if ball.xcor() > SCREEN_WIDTH/2 - 10 or ball.xcor() < -SCREEN_WIDTH/2 + 10:
            ball.bounce_x()

        if ball.ycor() > SCREEN_HEIGHT/2 - 10:
            ball.bounce_y()

        # Detect collision with paddle
        if ball.ycor() < paddle.ycor() + 10 and abs(ball.xcor() - paddle.xcor()) < PADDLE_HALF_WIDTH:
            ball.bounce_y()

        # Detect collision with bricks
        for brick in bricks:
            if ball.distance(brick) < 27:
                brick.goto(1000, 1000)
                bricks.remove(brick)
                ball.bounce_y()
                scoreboard.increase_score()
                break

        # Detect missing paddle
        if ball.ycor() < -SCREEN_HEIGHT/2 + 10:
            scoreboard.game_over()
            game_is_on = False

        # Check win condition
        if not bricks:
            scoreboard.win()
            game_is_on = False

    screen.exitonclick()

if __name__ == '__main__':
    main()
