import tkinter as tk
from tkinter import Canvas
from network import Network


class Shape:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, canvas: Canvas) -> None:
        pass


class Circle(Shape):
    def __init__(self, x: int, y: int, r: int = 20,
                 colour: str = "grey") -> None:
        super().__init__(x, y)
        self.r = r
        self.colour = colour

    def draw(self, canvas: Canvas) -> None:
        self.id = canvas.create_oval(
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
            fill=self.colour
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
        all_y = [z.x for z in self.network.zones.values()]

        max_x, min_x = max(all_x), min(all_x)
        max_y, min_y = max(all_y), min(all_y)

        frame_w = max_x - min_x
        frame_h = max_y - min_y

        scale = min(
            (self.canvas_w - 2 * self.padding) / frame_w if frame_w else 1,
            (self.canvas_h - 2 * self.padding) / frame_h if frame_h else 1
        )

        offset_x = (self.canvas_w - frame_w * scale) / 2 - min_x * scale
        offset_y = (self.canvas_h - frame_h * scale) / 2 - min_y * scale

        return int(scale), int(offset_x), int(offset_y)

    def visualise(self) -> None:
        graph = tk.Tk()
        canvas = tk.Canvas(graph, width=self.canvas_w, height=self.canvas_h)
        canvas.pack()

        scale, offset_x, offset_y = self.scale()

        for zone in self.network.zones.values():
            x = zone.x * scale + offset_x
            y = zone.y * scale + offset_y

            z = Circle(x, y, zone.max_drones * 20, zone.colour)
            z.draw(canvas)

        graph.mainloop()
