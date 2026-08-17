import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import turtle
import canvasvg

# Global references
screen = None
p = None
canvas_widget = None

# Default parameters
default_params = {
    "intervals": 2,
    "length": 200,
    "corners": 5,
    "offset": 1,
    "mode": "normal",
    "times": 12,
    "interval_change": 1,
    "length_change": 0,
    "angle_change": 0,
    "colors": ["red", "blue", "green", "orange", "purple"],
    "download_name": "my_drawing.svg"
}

current_params = default_params.copy()

def init_turtle(parent_frame):
    global screen, p, canvas_widget
    
    # Explicitly define width and height as integer pixel values
    canvas = tk.Canvas(parent_frame, width=600, height=600, bg="white")
    canvas.pack(fill=tk.BOTH, expand=True)
    
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("white")
    screen.tracer(0)  # Disable auto updates for faster rendering
    
    p = turtle.RawTurtle(screen)
    p.hideturtle()
    p.pensize(1)
    p.speed(0)

    canvas_widget = canvas

def create_inverse_pattern(intervals, length, corners, color, offset=1):
    global p
    if intervals <= 0 or corners <= 0:
        return
    
    angle = 360 / corners
    points = []
    interval_length = length / intervals

    p.penup()
    p.goto(length, 0)
    p.setheading(90)
    p.pendown()

    for i in range(corners * 2):
        points.append([])
        for j in range(intervals + 1):
            p.forward(interval_length)
            points[i].append(p.pos())

        if i % 2 == 0:
            p.left(angle)

    p.color(color)

    for i in range(corners):
        x_axis = ((i + offset) * 2) % (corners * 2)
        y_axis = (x_axis + offset) % (corners * 2)

        for j in range(intervals + 1):
            start_point = points[x_axis][j]
            end_point = points[y_axis][j]

            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

def create_overlapped_pattern(intervals, length, corners, color, offset=1):
    global p
    if intervals <= 0 or corners <= 0:
        return

    angle = 360 / corners
    points = []
    interval_length = length / intervals

    p.penup()
    p.setheading(0)
    p.goto(length // 2, -length // 2)
    p.setheading(90)
    p.pendown()

    for i in range(corners):
        points.append([])
        for j in range(intervals):
            p.forward(interval_length)
            points[i].append(p.pos())
        p.left(angle)

    p.color(color)

    for i in range(corners):
        next_axis = (i + offset) % corners

        for j in range(intervals):
            start_point = points[i][(j + 1) % intervals]
            end_point = points[next_axis][(j + 1) % intervals]

            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

def create_pattern(intervals, length, corners, color, offset=1):
    global p
    if intervals <= 0 or corners <= 0:
        return

    angle = 360 / corners
    points = []
    interval_length = length / intervals

    p.penup()
    p.goto(0, 0)
    p.pendown()

    for i in range(corners):
        points.append([])
        for j in range(intervals + 1):
            p.forward(interval_length)
            points[i].append(p.pos())
        p.backward(interval_length * (intervals + 1))
        p.right(angle)

    p.color(color)

    for i in range(corners):
        next_axis = (i + offset) % corners

        for j in range(intervals + 1):
            start_point = points[i][j]
            end_point = points[next_axis][intervals - j]

            p.penup()
            p.goto(start_point)
            p.pendown()
            p.goto(end_point)

def run_drawing():
    global p, screen
    
    intervals = int(sliders["intervals"].get())
    length = int(sliders["length"].get())
    corners = int(sliders["corners"].get())
    offset = int(sliders["offset"].get())
    times = int(sliders["times"].get())
    interval_change = int(sliders["interval_change"].get())
    length_change = int(sliders["length_change"].get())
    angle_change = int(sliders["angle_change"].get())
    mode = mode_var.get()
    colors = current_params["colors"]

    p.clear()
    p.penup()
    p.goto(0, 0)
    p.setheading(0)
    p.pendown()
    p.color("black")

    for i in range(times):
        color = colors[i % len(colors)]
        
        if intervals < 1:
            intervals = 1

        if mode == "overlapped":
            create_overlapped_pattern(intervals, length, corners, color, offset)
        elif mode == "inverse":
            create_inverse_pattern(intervals, length, corners, color, offset)
        else:
            create_pattern(intervals, length, corners, color, offset)

        p.penup()
        p.goto(0, 0)
        p.right(angle_change)
        p.color("black")

        intervals += interval_change
        length += length_change

    screen.update()

def download_svg():
    global canvas_widget
    if canvas_widget is None:
        messagebox.showwarning("No Canvas", "Run the drawing first.")
        return

    name = name_entry.get().strip()
    if not name:
        name = "my_drawing.svg"
    if not name.lower().endswith(".svg"):
        name += ".svg"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".svg",
        filetypes=[("SVG files", "*.svg")],
        initialfile=name
    )
    if not file_path:
        return

    try:
        canvas = screen.getcanvas()
        canvasvg.saveall(file_path, canvas)
        messagebox.showinfo("Saved", f"Drawing saved to:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save SVG:\n{e}")

def reset_defaults():
    for key, val in default_params.items():
        if key in sliders:
            sliders[key].set(val)
    mode_var.set(default_params["mode"])
    name_entry.delete(0, tk.END)
    name_entry.insert(0, default_params["download_name"])

# Build GUI
root = tk.Tk()
root.title("Turtle Pattern Generator")
root.geometry("1100x700")

# Left control panel
control_frame = ttk.Frame(root, padding=10)
control_frame.pack(side=tk.LEFT, fill=tk.Y)

slider_config = [
    ("intervals", 1, 50, 1),
    ("length", 50, 400, 10),
    ("corners", 3, 12, 1),
    ("offset", 1, 10, 1),
    ("times", 1, 50, 1),
    ("interval_change", -10, 10, 1),
    ("length_change", -50, 50, 5),
    ("angle_change", -30, 30, 1),
]

sliders = {}
for label_text, min_val, max_val, step in slider_config:
    frame = ttk.Frame(control_frame)
    frame.pack(fill=tk.X, pady=4)

    ttk.Label(frame, text=label_text.replace("_", " ").title(), width=18, anchor="w").pack(side=tk.LEFT)
    slider = ttk.Scale(frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL)
    slider.set(default_params[label_text])
    slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    value_label = ttk.Label(frame, text=str(int(slider.get())), width=5, anchor="e")
    value_label.pack(side=tk.LEFT, padx=(5, 0))

    def update_label(event, lbl=value_label, s=slider):
        lbl.config(text=str(int(s.get())))

    slider.bind("<B1-Motion>", update_label)
    slider.bind("<ButtonRelease-1>", update_label)

    sliders[label_text] = slider

# Mode selection
mode_frame = ttk.Frame(control_frame)
mode_frame.pack(fill=tk.X, pady=10)
ttk.Label(mode_frame, text="Mode:", width=18, anchor="w").pack(side=tk.LEFT)
mode_var = tk.StringVar(value=default_params["mode"])
for m in ["normal", "overlapped", "inverse"]:
    ttk.Radiobutton(mode_frame, text=m.title(), variable=mode_var, value=m).pack(side=tk.LEFT, padx=5)

# File name
name_frame = ttk.Frame(control_frame)
name_frame.pack(fill=tk.X, pady=6)
ttk.Label(name_frame, text="SVG file name:", width=18, anchor="w").pack(side=tk.LEFT)
name_entry = ttk.Entry(name_frame)
name_entry.insert(0, default_params["download_name"])
name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

# Buttons
btn_frame = ttk.Frame(control_frame)
btn_frame.pack(fill=tk.X, pady=15)

ttk.Button(btn_frame, text="Run", command=run_drawing).pack(fill=tk.X, pady=3)
ttk.Button(btn_frame, text="Download SVG", command=download_svg).pack(fill=tk.X, pady=3)
ttk.Button(btn_frame, text="Reset to Defaults", command=reset_defaults).pack(fill=tk.X, pady=3)

# Right drawing area
draw_frame = ttk.Frame(root)
draw_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Initialize turtle inside the draw_frame
init_turtle(draw_frame)

root.mainloop()