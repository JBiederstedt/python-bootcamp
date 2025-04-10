# Program takes a few seconds to start due to color extraction

import colorgram
from turtle import Turtle, Screen, colormode, exitonclick
import random

colormode(255)

Screen().setup(width=500, height=500)

timmy_the_turtle = Turtle()
timmy_the_turtle.hideturtle()
timmy_the_turtle.penup()

rgb_colors = []

colors = colorgram.extract('image.jpg', 30)

for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b

    rgb_colors.append((r, g, b))

for i in range(10):
    timmy_the_turtle.goto(-230, (-220 + i * 50))
    for _ in range(10):
        timmy_the_turtle.dot(20, random.choice(rgb_colors))
        timmy_the_turtle.penup()
        timmy_the_turtle.forward(50)

exitonclick()
