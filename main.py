import turtle
import canvasvg

screen = turtle.Screen()
screen.bgcolor("white")

p = turtle.Turtle()
p.pendown()
p.pensize(1)
p.speed(30)
p.hideturtle()

# global parameters
intervals = 20
lenght = 400
corners = 4
colors = ["red", "blue", "green", "orange", "purple"]
offset = 1


# inverse pattern parameters
inverse = False
overlapped = True

# after pattern parameters
download = False
name = "my_drawing.svg"

# repeat pattern parameters
times = 1
interval_change = -5
lenght_change = 0
angle_change = 0

def create_inverse_pattern(intervals, lenght, corners, color, offset=1):
    angle = 360/corners
    points = []
    interval_lenght = lenght/intervals

    p.penup()
    p.goto(0+lenght//2, 0-lenght//2)
    p.left(90)
    p.pendown()

    for i in range(corners):
        points.append([])
        for j in range(intervals+1):
            p.forward(interval_lenght)
            points[i].append(p.pos())
        p.left(angle)

    p.color(color)

    for i in range(corners):
        next_axis = (i + offset) % corners
        
        for j in range(intervals+ 1):
            start_point = points[i][j]
            end_point = points[next_axis][j]
            
            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

def create_overlapped_pattern(intervals, lenght, corners, color, offset=1):
    angle = 360 / corners
    points = []
    interval_lenght = lenght / intervals

    p.penup()
    p.setheading(0)
    p.goto(0 + lenght // 2, 0 - lenght // 2)
    p.left(90)
    p.pendown()

    for i in range(corners):
        points.append([])
        for j in range(intervals):
            p.forward(interval_lenght)
            points[i].append(p.pos())
            print(j)
        p.left(angle)

    p.color(color)

    for i in range(corners):
        next_axis = (i + offset) % corners
        
        for j in range(intervals):
            start_point = points[i][(j + 1) % (intervals)]
            end_point = points[next_axis][(j + 1) % (intervals)]
            print(j)
            
            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

def create_pattern(intervals, lenght, corners, color, offset=1):
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
        next_axis = (i + offset) % corners
        
        for j in range(intervals+ 1):
            start_point = points[i][j]
            end_point = points[next_axis][intervals - j]
            
            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

def start(intervals, lenght, corners, colors, offset, times, interval_change, lenght_change, angle_change, inverse, overlapped, download=False, name="my_drawing.svg"):
    for i in range(times):
        if overlapped:
            create_overlapped_pattern(intervals, lenght, corners, colors[i % len(colors)], offset)
        elif inverse:
            create_inverse_pattern(intervals, lenght, corners, colors[i % len(colors)], offset)
        else:
            create_pattern(intervals, lenght, corners, colors[i % len(colors)], offset)
        p.penup()
        p.goto(0, 0)
        p.right(angle_change)
        p.color("black")
        intervals += interval_change
        lenght += lenght_change

    if download:
        canvas = turtle.getscreen().getcanvas()
        canvasvg.saveall(name, canvas)

def main():
    start(intervals, lenght, corners, colors, offset, times, interval_change, lenght_change, angle_change, inverse, overlapped)

main()
screen.tracer(0)
screen.update()
screen.mainloop()