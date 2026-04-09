# 1. Base Shape Class System
import random
import tkinter as tk


class Shape:
    def __init__(self, x, y, color="black"):
        self.x = x
        self.y = y
        self.color = color
        self.id = None  # canvas object id

    def draw(self, canvas):
        pass


class Circle(Shape):
    def __init__(self, x, y, r=20, color="blue"):
        super().__init__(x, y, color)
        self.r = r

    def draw(self, canvas):
        self.id = canvas.create_oval(
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
            fill=self.color
        )


root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

c = Circle(200, 150)
c.draw(canvas)

root.mainloop()


# 2. Multiple Shapes Playground


# class Circle:
#     def __init__(self, x, y, r, color):
#         self.x, self.y, self.r, self.color = x, y, r, color

#     def draw(self, canvas):
#         canvas.create_oval(self.x-self.r, self.y-self.r,
#                            self.x+self.r, self.y+self.r,
#                            fill=self.color)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=500, height=400)
# canvas.pack()

# colors = ["red", "green", "blue", "orange"]

# for _ in range(10):
#     c = Circle(random.randint(50, 450), random.randint(50, 350),
#                random.randint(10, 30), random.choice(colors))
#     c.draw(canvas)

# root.mainloop()


# 3. Animation (Moving Shapes)


# class Ball:
#     def __init__(self, canvas, x, y):
#         self.canvas = canvas
#         self.id = canvas.create_oval(x, y, x+30, y+30, fill="blue")
#         self.vx = 3
#         self.vy = 2

#     def move(self):
#         self.canvas.move(self.id, self.vx, self.vy)


# def animate():
#     ball.move()
#     root.after(20, animate)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# ball = Ball(canvas, 50, 50)
# animate()

# root.mainloop()


# 4. Mouse Interaction (Click + Drag)


# class DraggableCircle:
#     def __init__(self, canvas, x, y):
#         self.canvas = canvas
#         self.id = canvas.create_oval(x, y, x+40, y+40, fill="green")

#         canvas.tag_bind(self.id, "<Button-1>", self.start_drag)
#         canvas.tag_bind(self.id, "<B1-Motion>", self.drag)

#     def start_drag(self, event):
#         self.last_x = event.x
#         self.last_y = event.y

#     def drag(self, event):
#         dx = event.x - self.last_x
#         dy = event.y - self.last_y
#         self.canvas.move(self.id, dx, dy)
#         self.last_x = event.x
#         self.last_y = event.y


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# DraggableCircle(canvas, 100, 100)

# root.mainloop()


# 5. Keyboard Controls


# class Player:
#     def __init__(self, canvas):
#         self.canvas = canvas
#         self.id = canvas.create_rectangle(180, 130, 220, 170, fill="red")

#     def move(self, dx, dy):
#         self.canvas.move(self.id, dx, dy)


# def key_handler(event):
#     if event.keysym == "Up":
#         player.move(0, -10)
#     elif event.keysym == "Down":
#         player.move(0, 10)
#     elif event.keysym == "Left":
#         player.move(-10, 0)
#     elif event.keysym == "Right":
#         player.move(10, 0)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# player = Player(canvas)
# root.bind("<Key>", key_handler)

# root.mainloop()


# 6. Simple Physics (Bouncing Ball)


# class Ball:
#     def __init__(self, canvas):
#         self.canvas = canvas
#         self.id = canvas.create_oval(50, 50, 80, 80, fill="blue")
#         self.vx = 4
#         self.vy = 3

#     def update(self):
#         x1, y1, x2, y2 = self.canvas.coords(self.id)

#         if x1 <= 0 or x2 >= 400:
#             self.vx *= -1
#         if y1 <= 0 or y2 >= 300:
#             self.vy *= -1

#         self.canvas.move(self.id, self.vx, self.vy)


# def loop():
#     ball.update()
#     root.after(20, loop)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# ball = Ball(canvas)
# loop()

# root.mainloop()


# 7. Shape Relationships (Connected Nodes)


# class Node:
#     def __init__(self, canvas, x, y):
#         self.canvas = canvas
#         self.x, self.y = x, y
#         self.id = canvas.create_oval(x-10, y-10, x+10, y+10, fill="black")


# def connect(canvas, n1, n2):
#     return canvas.create_line(n1.x, n1.y, n2.x, n2.y)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# n1 = Node(canvas, 100, 150)
# n2 = Node(canvas, 300, 150)

# connect(canvas, n1, n2)

# root.mainloop()


# 8. Zoom & Coordinate System (Basic Scaling)

# scale = 1.0


# def zoom(event):
#     global scale
#     factor = 1.1 if event.delta > 0 else 0.9
#     scale *= factor
#     canvas.scale("all", event.x, event.y, factor, factor)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# canvas.create_rectangle(100, 100, 200, 200, fill="blue")

# canvas.bind("<MouseWheel>", zoom)

# root.mainloop()


# 9. Visual Feedback (Selection Highlight)

# selected = None


# def select(event):
#     global selected
#     item = canvas.find_closest(event.x, event.y)[0]

#     if selected:
#         canvas.itemconfig(selected, outline="black", width=1)

#     selected = item
#     canvas.itemconfig(selected, outline="red", width=3)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# canvas.create_rectangle(50, 50, 150, 150, fill="blue")
# canvas.create_rectangle(200, 50, 300, 150, fill="green")

# canvas.bind("<Button-1>", select)

# root.mainloop()


# 10. Mini Editor (Add Shapes on Click)


# def add_shape(event):
#     r = 20
#     color = random.choice(["red", "blue", "green"])
#     canvas.create_oval(event.x-r, event.y-r,
#                        event.x+r, event.y+r,
#                        fill=color)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# canvas.bind("<Button-1>", add_shape)

# root.mainloop()


# 11. Debug Visualization (Velocity Vectors)


# class Ball:
#     def __init__(self, canvas):
#         self.canvas = canvas
#         self.x, self.y = 100, 100
#         self.vx, self.vy = 3, 2
#         self.id = canvas.create_oval(90, 90, 110, 110, fill="blue")
#         self.vector = canvas.create_line(0, 0, 0, 0, fill="red")

#     def update(self):
#         self.x += self.vx
#         self.y += self.vy

#         self.canvas.coords(self.id, self.x-10, self.y-10,
#                            self.x+10, self.y+10)

#         # draw velocity vector
#         self.canvas.coords(self.vector,
#                            self.x, self.y,
#                            self.x + self.vx*10,
#                            self.y + self.vy*10)


# def loop():
#     ball.update()
#     root.after(20, loop)


# root = tk.Tk()
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()

# ball = Ball(canvas)
# loop()

# root.mainloop()
