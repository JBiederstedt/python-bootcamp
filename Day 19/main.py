from turtle import Turtle, Screen
import random

screen = Screen()
screen.setup(width=500, height=400)

race_is_on = False
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
turtles = []
start_y = -100

for i in range(len(colors)):
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[i])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=start_y + i * 40)
    turtles.append(new_turtle)

user_bet = screen.textinput(
    title="Make your bet",
    prompt="Which turtle will win the race? Enter a color:"
)

if user_bet:
    race_is_on = True

while race_is_on:
    for turtle in turtles:
        if turtle.xcor() > 220:
            race_is_on = False
            winning_color = turtle.pencolor()
            if winning_color == user_bet:
                print(f"\nYou've won. The {winning_color} turtle is the winner!")
            else:
                print(f"\nYou've lost. The {winning_color} turtle is the winner!")

        random_distance = random.randint(0, 10)
        turtle.forward(random_distance)

screen.exitonclick()
