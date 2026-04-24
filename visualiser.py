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

        elif colour == "rainbow":
            return "rainbow"

        try:
            canvas.winfo_rgb(colour)
            return colour
        except tk.TclError:
            print(
                f"Oops. The colour '{colour}' in map config is not on our "
                f"colour palette. Using default colour '{default}' instead.")
            return default


class Circle(Shape):
    def __init__(self, x: int, y: int, radius: int,
                 colour: str) -> None:
        super().__init__(x, y)
        self.r = radius
        self.colour = colour if colour else "grey"

    def draw(self, canvas: Canvas) -> None:
        valid_colour = self.check_colour(canvas, self.colour, "lightblue")
        if valid_colour == "rainbow":
            colours = [
                "#E27F7F", "#E4A15D", "#E2E27B",
                "#76D176", "#648BE0", "#538366",
                "#6E608F"]
            step = self.r // len(colours)

            for i, colour in enumerate(colours):
                r = self.r - i * step
                canvas.create_oval(
                    self.x - r, self.y - r,
                    self.x + r, self.y + r,
                    fill=colour,
                    outline="#ffffff",
                    width=2)
            return

        self.draw_circle = canvas.create_oval(
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
            fill=valid_colour, outline="#ffffff", width=3)


class Visualiser:
    def __init__(self, network: Network, canvas_w: int,
                 canvas_h: int, padding: int,
                 min_zoom: float = 30.0,
                 max_zoom: float = 220.0) -> None:
        self.network = network
        self.canvas_w = canvas_w
        self.sidebar_h = canvas_h * 0.2
        self.canvas_h = canvas_h - self.sidebar_h
        self.padding = padding
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom

    def scale(self) -> tuple[float, float, float]:
        all_x = [z.x for z in self.network.zones.values()]
        all_y = [z.y for z in self.network.zones.values()]

        max_x, min_x = max(all_x), min(all_x)
        max_y, min_y = max(all_y), min(all_y)

        frame_w = max_x - min_x
        frame_h = max_y - min_y

        scale = min(
            (self.canvas_w - 2 * self.padding) / frame_w
            if frame_w else float("inf"),
            (self.canvas_h - 2 * self.padding) / frame_h
            if frame_h else float("inf")
        )

        if scale == float("inf"):
            scale = 1.0

        scale = max(self.min_zoom, min(scale, self.max_zoom))

        offset_x = ((self.canvas_w - (frame_w * scale)) / 2) - (min_x * scale)
        offset_y = ((self.canvas_h - (frame_h * scale)) / 2) - (min_y * scale)

        return scale, offset_x, offset_y

    def connect(self, canvas: Canvas, x1: int, y1: int,
                x2: int, y2: int) -> int:
        return canvas.create_line(x1, y1, x2, y2,
                                  width=2, fill="LavenderBlush4")

    def visualise(self) -> None:
        self.graph = tk.Tk()
        self.graph.title("Fly-in Visualiser")

        canvas = tk.Canvas(self.graph, width=self.canvas_w,
                           height=self.canvas_h, bg="#88bcd1")
        canvas.pack(side="top", fill="both", expand=True)

        sidebar = tk.Frame(self.graph, height=self.sidebar_h, bg="#91BE90")
        sidebar.pack(side="bottom", fill="both")

        scale, offset_x, offset_y = self.scale()
        max_allowed_radius = max(4, int(scale * 0.45))
        radius = max(3, int(scale * 0.15))

        for conn in self.network.connections:
            x1 = int(conn.zone1.x * scale + offset_x)
            y1 = int(conn.zone1.y * scale + offset_y)

            x2 = int(conn.zone2.x * scale + offset_x)
            y2 = int(conn.zone2.y * scale + offset_y)

            self.connect(canvas, x1, y1, x2, y2)

        for zone in self.network.zones.values():
            x = int(zone.x * scale + offset_x)
            y = int(zone.y * scale + offset_y)

            growth_bonus = zone.max_drones * int(scale * 0.05)
            current_radius = min(radius + growth_bonus, max_allowed_radius)

            z = Circle(x, y, current_radius, zone.colour)
            z.draw(canvas)

        # graph.bind("<Right>", self.next_step)
        # graph.bind("<Left>", self.prev_step)
        self.graph.bind("<Escape>", self.quit)

        self.graph.mainloop()

    def quit(self, event=None) -> None:
        """Close the visualiser window."""
        self.graph.destroy()
