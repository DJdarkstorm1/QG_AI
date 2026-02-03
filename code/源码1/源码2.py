import turtle # 导包

turtle.showturtle() # 显示箭头
turtle.write("Hello World") # 写字
turtle.forward(100) # 向前移动100像素
turtle.left(90)  # 左转90°
turtle.color("red") # 设置颜色为红色
turtle.forward(100)
turtle.left(135)  # 左转135°
turtle.color("blue") # 设置颜色为蓝色
turtle.forward(141)
turtle.left(45)
turtle.color("green")
turtle.forward(141)
turtle.penup()
turtle.goto(-100,-100)
turtle.pendown()
turtle.forward(100)
turtle.done()