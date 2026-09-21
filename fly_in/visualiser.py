"""GUI visualiser using tkinter to render the network and simulation."""

import tkinter as tk
from tkinter import Canvas
from network import Network
from parser import MapParser
from typing import Any


class Shape:
    """Base drawable shape with an (x,y) position."""

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def draw(self, canvas: Canvas) -> None:
        """Draw the shape on canvas."""
        pass

    def check_colour(self, canvas: Canvas, colour: str, default: str) -> str:
        """Validate a colour that tkinter recognises, else raise exception."""

        if not colour:
            return default

        if colour == "rainbow":
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
    """Circle shape with customised radius visualising a zone."""

    def __init__(self, x: int, y: int, radius: int,
                 colour: str, name: str) -> None:
        super().__init__(x, y)
        self.r = radius
        self.colour = colour if colour else "grey"
        self.zone_tag = name

    def draw(self, canvas: Canvas) -> None:
        """Render the circle on the canvas, supporting a rainbow fill."""

        valid_colour = self.check_colour(canvas, self.colour, "grey")
        if valid_colour == "rainbow":
            colours = [
                "#E27F7F", "#E2E27B", "#76D176", "#648BE0", "#6E608F"]
            step = self.r // len(colours)

            for i, colour in enumerate(colours):
                r = self.r - i * step
                canvas.create_oval(
                    self.x - r, self.y - r,
                    self.x + r, self.y + r,
                    fill=colour,
                    outline="",
                    tags=self.zone_tag)
            return

        self.draw_circle = canvas.create_oval(
            self.x - self.r, self.y - self.r,
            self.x + self.r, self.y + self.r,
            fill=valid_colour, outline="", tags=self.zone_tag)

    def hover_effect(self, canvas: Canvas, info_text_id: int) -> None:
        """Attach hover bindings that show/hide a zone info text."""

        self.info_text = info_text_id
        canvas.tag_bind(self.zone_tag, "<Enter>",
                        lambda event: self.show_info(canvas))
        canvas.tag_bind(self.zone_tag, "<Leave>",
                        lambda event: self.hide_info(canvas))

    def show_info(self, canvas: Canvas) -> None:
        """Internal: make the zone info text visible on hover."""
        if self.info_text is not None:
            canvas.itemconfigure(self.info_text, state="normal")

    def hide_info(self, canvas: Canvas) -> None:
        """Internal: hide the zone info text when hover ends."""
        if self.info_text is not None:
            canvas.itemconfigure(self.info_text, state="hidden")


class Triangle(Shape):
    """Simple triangular marker used to draw drones on the map."""

    def __init__(self, x: int, y: int, size: int) -> None:
        super().__init__(x, y)
        self.size = size

    def draw(self, canvas: Canvas) -> None:
        """Draw the triangular drone marker on the canvas."""

        canvas.create_polygon(
            self.x,
            self.y - self.size,
            self.x - self.size,
            self.y + self.size,
            self.x + self.size,
            self.y + self.size,
            fill="#4E4683",
            outline="#FFFFFF")


class Visualiser:
    """Visualise a Network and optional simulation history with tkinter."""

    def __init__(self, network: Network, canvas_w: int,
                 canvas_h: int, padding: int,
                 parser: MapParser,
                 history: list[dict[str, str]] | None = None,
                 min_zoom: float = 0.5,
                 max_zoom: float = 150.0) -> None:
        self.parser = parser
        self.network = network
        self.canvas_w = canvas_w
        self.sidebar_h = int(canvas_h * 0.2)
        self.canvas_h = int(canvas_h - self.sidebar_h)
        self.padding = padding
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.history = history or []
        self.current_step = 0
        self.turn_label: tk.Label | None = None

    def scale(self) -> tuple[float, float, float]:
        """Return mapping network coords to canvas."""

        if not self.network.zones:
            return 1.0, 0.0, 0.0

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
        """Draw a connection line and return the canvas id."""

        return canvas.create_line(x1, y1, x2, y2,
                                  width=2, fill="#9b94b6")

    def draw_drones(self, canvas: Canvas, scale: float,
                    offset_x: float, offset_y: float) -> None:
        """Draw drone markers for the current history step or live state."""

        if self.history:
            positions: dict[str, list[str]] = {}
            for drone_id, zone_name in self.history[self.current_step].items():
                positions.setdefault(zone_name, []).append(drone_id)
        else:
            positions = {}
            for zone in self.network.zones.values():
                positions[zone.name] = [
                    d.drone_id for d in zone.current_drones
                ]

        for zone_name, drone_ids in positions.items():
            zone = self.network.zones[zone_name]
            zx = int(zone.x * scale + offset_x)
            zy = int(zone.y * scale + offset_y)
            for drone_id in drone_ids:
                Triangle(zx, zy, 5).draw(canvas)
                canvas.create_text(
                    zx, zy + 19, text=drone_id, fill="#5F5843")

    def draw_frame(self, canvas: Canvas) -> None:
        """Clear and redraw the visual frame (zones, links, drones)."""

        canvas.delete("all")
        self.update_turn_info()

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
            zone_scale = zone.max_drones * int(scale * 0.05)
            current_radius = min(radius + zone_scale, max_allowed_radius)
            z = Circle(x, y, current_radius, zone.colour, zone.name)
            z.draw(canvas)

            zone_info = (
                f"{zone.name} -- [{zone.zone_type.upper()}]\n"
                f"-- max. {zone.max_drones} drones allowed")
            info_text_id = canvas.create_text(
                x, y - current_radius - 28,
                text=zone_info, fill="#2f2757",
                state="hidden", justify="center")
            z.hover_effect(canvas, info_text_id)

            if "start" in zone.name:
                canvas.create_text(x, y, text="START", fill="white")
            elif "goal" in zone.name:
                canvas.create_text(x, y, text="GOAL", fill="white")

        self.draw_drones(canvas, scale, offset_x, offset_y)

    def visualise(self) -> None:
        """Create the tkinter window and start the visualiser loop."""

        self.graph = tk.Tk()
        self.graph.title("Fly-in Visualiser")

        canvas = tk.Canvas(self.graph, width=self.canvas_w,
                           height=self.canvas_h, bg="#b0e0e6")
        canvas.pack(side="top", fill="both", expand=True)

        self.sidebar_config()

        self.draw_frame(canvas)

        if self.history:
            self.graph.bind("<Right>", lambda event: self.next_step(canvas))
            self.graph.bind("<Left>", lambda event: self.prev_step(canvas))

        self.graph.bind("<Escape>", self.quit)

        self.graph.mainloop()

    def next_step(self, canvas: Canvas) -> None:
        """Advance to the next history step and redraw the frame."""

        if self.current_step + 1 < len(self.history):
            self.current_step += 1
            self.draw_frame(canvas)

    def prev_step(self, canvas: Canvas) -> None:
        """Step back one history turn and redraw the frame."""

        if self.current_step > 0:
            self.current_step -= 1
            self.draw_frame(canvas)

    def update_turn_info(self) -> None:
        """Update the sidebar turn label to reflect the current step."""

        if self.turn_label is not None:
            total = len(self.history) - 1 if self.history else 1
            self.turn_label.config(
                text=f"Turns stats     :   {self.current_step}  /  {total}"
            )

    def quit(self, event: Any = None) -> None:
        """Close the visualiser window."""
        self.graph.destroy()

    def sidebar_config(self) -> None:
        """Create and layout the bottom sidebar with controls and info."""

        self.sidebar = tk.Frame(
            self.graph, height=self.sidebar_h, bg="LavenderBlush3")
        self.sidebar.pack(side="bottom", fill="x")

        controls = tk.Frame(self.sidebar, bg="LavenderBlush3")
        controls.pack(side="left", expand=True, pady=20)
        for line in [
            "CONTROLS",
            "===========================",
            "[-->]    Next turn        ",
            "[<--]    Previous turn  ",
            "[ESC]   Quit visualiser"
        ]:
            tk.Label(controls, text=line, bg="LavenderBlush3",
                     fg="#443b69", anchor="w").pack()

        filepath = self.parser.filepath
        drones_total = self.parser.drones_total
        infos = tk.Frame(self.sidebar, bg="LavenderBlush3")
        infos.pack(side="right", expand=True, pady=20)
        tk.Label(infos, text="MAP DETAILS", bg="LavenderBlush3",
                 fg="#443b69", anchor="w").pack()
        for line in [
            "=========================================="
            "==========================================",
            f"Map file path  :   {filepath}   ",
            f"Total drones   :   {drones_total}",
        ]:
            tk.Label(infos, text=line, bg="LavenderBlush3",
                     fg="#443b69", anchor="w").pack(fill="x")

        total_turns = len(self.history) - 1 if self.history else 1
        self.turn_label = tk.Label(
            infos,
            bg="LavenderBlush3",
            fg="#443b69",
            anchor="w",
            text=f"Turns stats     :   {self.current_step}  /  {total_turns}",
        )
        self.turn_label.pack(fill="x")
