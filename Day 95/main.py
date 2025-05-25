import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.setup(width=700, height=700)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.tracer(0)

# Score
score = 0
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.color("white")
score_pen.penup()
score_pen.goto(0, 310)
score_pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

# Player
player = turtle.Turtle()
player.shape("triangle")
player.color("green")
player.penup()
player.goto(0, -250)
player.setheading(90)
player_speed = 30

# Bullet
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(0.2, 0.8)
bullet.penup()
bullet.hideturtle()
bullet_speed = 20
bullet_state = "ready"

# Enemies
enemy_speed = 20
enemies = []
for _ in range(30):
    enemy = turtle.Turtle()
    enemy.shape("circle")
    enemy.color("red")
    enemy.penup()
    x = random.randint(-300, 300)
    y = random.randint(50, 250)
    enemy.goto(x, y)
    enemies.append(enemy)

# Barriers
barriers = []
barrier_positions = [(-250, -100), (-100, -100), (100, -100), (250, -100)]
for (bx, by) in barrier_positions:
    for row in range(3):
        for col in range(5):
            barrier = turtle.Turtle()
            barrier.shape("square")
            barrier.color("blue")
            barrier.penup()
            barrier.shapesize(stretch_wid=0.5, stretch_len=1)
            x = bx + (col * 20)
            y = by + (row * 20)
            barrier.goto(x, y)
            barriers.append(barrier)

# Initial draw
screen.update()

# Movement functions
def move_left():
    x = player.xcor() - player_speed
    if x < -330:
        x = -330
    player.setx(x)

def move_right():
    x = player.xcor() + player_speed
    if x > 330:
        x = 330
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        bullet.goto(player.xcor(), player.ycor() + 10)
        bullet.showturtle()

# Game functions
def move_enemies():
    global enemy_speed
    move_down = False
    for e in enemies:
        x = e.xcor() + enemy_speed
        e.setx(x)
        if e.xcor() > 320 or e.xcor() < -320:
            move_down = True
    if move_down:
        enemy_speed *= -1
        for e in enemies:
            e.sety(e.ycor() - 40)
    # check game over
    for e in enemies:
        if e.ycor() < -230:
            game_over()
            return
    screen.update()
    screen.ontimer(move_enemies, 1000)

def move_bullet():
    global bullet_state, score
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + bullet_speed)
        # out of bounds
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"
        else:
            # collision with enemies
            for e in enemies:
                if bullet.distance(e) < 20:
                    # reset bullet
                    bullet.hideturtle()
                    bullet_state = "ready"
                    # reset enemy
                    e.goto(random.randint(-300,300), random.randint(50,250))
                    score += 10
                    score_pen.clear()
                    score_pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
                    break
            # collision with barrier
            for b in barriers:
                if bullet.distance(b) < 20:
                    b.hideturtle()
                    barriers.remove(b)
                    bullet.hideturtle()
                    bullet_state = "ready"
                    break
    screen.update()
    screen.ontimer(move_bullet, 20)

def game_over():
    for e in enemies:
        e.hideturtle()
    player.hideturtle()
    bullet.hideturtle()
    for b in barriers:
        b.hideturtle()
    score_pen.goto(0,0)
    score_pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))

# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Start game loops
move_enemies()
move_bullet()
screen.mainloop()
