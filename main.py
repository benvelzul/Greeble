import turtle

screen = turtle.Screen()
screen.bgcolor("white")

p = turtle.Turtle()
p.pendown()
p.pensize(1)
p.speed(10)
p.hideturtle()

intervals = 25
lenght = 300
corners = 5
color = "blue"

def create_pattern(intervals, lenght, corners, color):
    angle = 360/corners
    points = []
    interval_lenght = lenght/intervals

    for i in range(corners):
        points.append([])
        for j in range(intervals+1):
            p.forward(interval_lenght)
            points[i].append(p.pos())
        p.back(interval_lenght * (intervals + 1))
        p.right(angle)

    p.color(color)

    for i in range(corners):
        next_axis = (i + 1) % corners
        
        for j in range(intervals+ 1):
            start_point = points[i][j]
            end_point = points[next_axis][intervals - j]
            
            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

create_pattern(intervals, lenght, corners, color)

screen.tracer(0)

screen.update()
screen.mainloop()