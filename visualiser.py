import tkinter as tk
from tkinter import Canvas
from network import Network


class Shape:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, canvas: Canvas) -> None:
        pass

    def check_colour(self, canvas: Canvas, colour: str, default: str) -> str:
        if not colour:
            return default

        try:
            canvas.winfo_rgb(colour)
            return colour
        except tk.TclError:
            print(
                f"Invalid color '{colour}' in maps detected. "
                f"Default colour '{default}' applied to visualiser.")
            return default


class Circle(Shape):
    def __init__(self, x: int, y: int, radius: int,
                 colour: str) -> None:
        super().__init__(x, y)
        self.r = radius
        self.colour = colour if colour else "grey"

    def draw(self, canvas: Canvas) -> None:
        valid_colour = self.check_colour(canvas, self.colour, "green")
        self.draw_circle = canvas.create_oval(
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
            fill=valid_colour
        )


class Visualiser:
    def __init__(self, network: Network, canvas_w: int,
                 canvas_h: int, padding: int) -> None:
        self.network = network
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.padding = padding

    def scale(self) -> tuple[int, int, int]:
        all_x = [z.x for z in self.network.zones.values()]
        all_y = [z.y for z in self.network.zones.values()]

        max_x, min_x = max(all_x), min(all_x)
        max_y, min_y = max(all_y), min(all_y)

        frame_w = max_x - min_x
        frame_h = max_y - min_y

        scale = min(
            (self.canvas_w - 2 * self.padding) / frame_w if frame_w else 1,
            (self.canvas_h - 2 * self.padding) / frame_h if frame_h else 1
        )

        offset_x = ((self.canvas_w - (frame_w * scale)) / 2) - (min_x * scale)
        offset_y = ((self.canvas_h - (frame_h * scale)) / 2) - (min_y * scale)

        return int(scale), int(offset_x), int(offset_y)

    def connect(self, canvas: Canvas, x1: int, y1: int,
                x2: int, y2: int) -> int:
        return canvas.create_line(x1, y1, x2, y2, width=2, fill="black")

    def visualise(self) -> None:
        graph = tk.Tk()
        graph.title("Fly-in Visualiser")

        # radius = 10
        canvas = tk.Canvas(graph, width=self.canvas_w,
                           height=self.canvas_h, bg="white")
        canvas.pack()

        scale, offset_x, offset_y = self.scale()
        max_allowed_radius = max(4, int(scale * 0.45))
        radius = max(3, int(scale * 0.15))

        for conn in self.network.connections:
            x1 = conn.zone1.x * scale + offset_x
            y1 = conn.zone1.y * scale + offset_y

            x2 = conn.zone2.x * scale + offset_x
            y2 = conn.zone2.y * scale + offset_y

            self.connect(canvas, x1, y1, x2, y2)

        for zone in self.network.zones.values():
            x = zone.x * scale + offset_x
            y = zone.y * scale + offset_y

            growth_bonus = zone.max_drones * int(scale * 0.05)
            current_radius = min(radius + growth_bonus, max_allowed_radius)

            z = Circle(x, y, current_radius, zone.colour)
            z.draw(canvas)

            canvas.create_text(x, y - current_radius - 10, text=zone.name)

        graph.mainloop()
