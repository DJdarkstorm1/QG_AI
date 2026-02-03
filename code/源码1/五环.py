import turtle

high=60

turtle.width(10)
turtle.speed(20)
turtle.color("black")
turtle.circle(50)

turtle.color("blue")
turtle.penup()
turtle.goto(-120,0)
turtle.pendown()
turtle.circle(50)

turtle.color("red")
turtle.penup()
turtle.goto(120,0)
turtle.pendown()
turtle.circle(50)

turtle.color("green")
turtle.penup()
turtle.goto(60,-110+high)
turtle.pendown()
turtle.circle(50)

turtle.color("yellow")
turtle.penup()
turtle.goto(-60,-110+high)
turtle.pendown()
turtle.circle(50)

turtle.done()
