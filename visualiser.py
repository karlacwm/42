import tkinter as tk
import random
from collections import defaultdict
from tkinter import Canvas


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
    def __init__(self,
                 network,
                 canvas_w: int = 800,
                 canvas_h: int = 600,
                 padding: int = 50) -> None:
        self.network = network
        self.canvas_w = max(canvas_w, 1500)
        self.canvas_h = max(canvas_h, 1200)
        self.padding = padding

    def scale(self) -> tuple[float, float, float]:
        """Return scale and offsets so the map fits on canvas."""
        if not self.network.zones:
            return 1.0, 0.0, 0.0

        xs = [zone.x for zone in self.network.zones.values()]
        ys = [zone.y for zone in self.network.zones.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        graph_w = max(max_x - min_x, 1)
        graph_h = max(max_y - min_y, 1)

        usable_w = max(self.canvas_w - (self.padding * 2), 1)
        usable_h = max(self.canvas_h - (self.padding * 2), 1)

        scale = min(usable_w / graph_w, usable_h / graph_h)
        offset_x = (self.canvas_w - (graph_w * scale)) / 2 - (min_x * scale)
        offset_y = (self.canvas_h - (graph_h * scale)) / 2 - (min_y * scale)
        return scale, offset_x, offset_y

    def _layout(self) -> tuple[float, float, float, int]:
        """Return drawing transform and an appropriate zone radius."""
        if not self.network.zones:
            return 1.0, 0.0, 0.0, 8

        xs = [zone.x for zone in self.network.zones.values()]
        ys = [zone.y for zone in self.network.zones.values()]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        graph_w = max(max_x - min_x, 1)
        graph_h = max(max_y - min_y, 1)

        side_margin = max(self.padding, 45)
        top_margin = max(self.padding, 70)
        label_margin = 16

        rough_usable_w = max(self.canvas_w - (side_margin * 2), 1)
        rough_usable_h = max(self.canvas_h - top_margin - side_margin, 1)
        rough_scale = min(rough_usable_w / graph_w, rough_usable_h / graph_h)

        radius = int(max(6, min(20, rough_scale * 0.12)))

        left = side_margin + radius
        right = side_margin + radius
        top = top_margin + radius + label_margin
        bottom = side_margin + radius

        usable_w = max(self.canvas_w - left - right, 1)
        usable_h = max(self.canvas_h - top - bottom, 1)
        scale = min(usable_w / graph_w, usable_h / graph_h)

        offset_x = left - (min_x * scale) + \
            ((usable_w - (graph_w * scale)) / 2)
        offset_y = top - (min_y * scale) + ((usable_h - (graph_h * scale)) / 2)
        return scale, offset_x, offset_y, radius

    def connect(self,
                canvas: Canvas,
                x1: int,
                y1: int,
                x2: int,
                y2: int) -> None:
        """Draw one connection line."""
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    def _safe_colour(self, colour: str, default: str = "lightblue") -> str:
        """Return a Tk-compatible colour string."""
        if not colour:
            return default

        if colour.strip().lower() == "rainbow":
            return "rainbow"

        try:
            self.canvas.winfo_rgb(colour)
            return colour
        except tk.TclError:
            print(
                f"Invalid color '{colour}' in maps detected. "
                f"Default colour '{default}' applied to visualiser.")
            return default

    def _draw_rainbow_zone(self,
                           x: int,
                           y: int,
                           radius: int) -> None:
        """Draw a zone with rainbow slices."""
        colours = [
            "#FF0000",  # red
            "#FF7F00",  # orange
            "#FFFF00",  # yellow
            "#00FF00",  # green
            "#0000FF",  # blue
            "#4B0082",  # indigo
            "#8F00FF",  # violet
        ]
        extent = 360 / len(colours)

        for i, colour in enumerate(colours):
            start = i * extent
            self.canvas.create_arc(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                start=start,
                extent=extent,
                style=tk.PIESLICE,
                outline="",
                fill=colour,
            )

        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline="black",
            width=1,
        )

    def visualise(self, history: list) -> None:
        self.history = history
        self.current_step = 0
        self.max_step = len(history) - 1
        self.zone_drone_counts: dict[str, int] = {}

        self.graph = tk.Tk()
        self.graph.title("Fly-in Visualiser")

        self.main_frame = tk.Frame(self.graph)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.canvas_w,
            height=self.canvas_h,
            bg="white",
            highlightthickness=0,
        )
        self.canvas.pack(side="left", fill="both", expand=False)

        self.sidebar = tk.Frame(
            self.main_frame,
            width=320,
            bg="#f3f5f7",
            padx=12,
            pady=12,
        )
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # Add a text label at the top left to show the Turn number
        self.turn_text = self.canvas.create_text(
            50, 20, text=f"Turn: {self.current_step}", font=("Arial", 14, "bold"), anchor="w")

        # Key Bindings to move through time!
        self.graph.bind("<Right>", self.next_step)
        self.graph.bind("<Left>", self.prev_step)
        self.graph.bind("<Escape>", self.quit)

        # Draw the first frame (Turn 0)
        self.draw_frame()

        self.graph.mainloop()

    def _build_sidebar(self) -> None:
        """Create side controls and hover information panels."""
        tk.Label(
            self.sidebar,
            text="Controls",
            anchor="w",
            bg="#f3f5f7",
            font=("Arial", 13, "bold"),
        ).pack(fill="x", pady=(0, 8))

        controls = [
            "Right Arrow : Next turn",
            "Left Arrow   : Previous turn",
            "ESC            : Quit visualiser",
        ]
        for line in controls:
            tk.Label(
                self.sidebar,
                text=line,
                anchor="w",
                justify="left",
                bg="#f3f5f7",
                font=("Arial", 11),
            ).pack(fill="x", pady=2)

        tk.Frame(self.sidebar, bg="#d9dee3", height=2).pack(
            fill="x", pady=(12, 12))

        tk.Label(
            self.sidebar,
            text="Zone Info (hover)",
            anchor="w",
            bg="#f3f5f7",
            font=("Arial", 13, "bold"),
        ).pack(fill="x", pady=(0, 8))

        self.zone_info_var = tk.StringVar()
        self.zone_info_var.set("Move the mouse over a zone to see details.")

        tk.Label(
            self.sidebar,
            textvariable=self.zone_info_var,
            anchor="nw",
            justify="left",
            wraplength=290,
            bg="#ffffff",
            relief="solid",
            bd=1,
            padx=10,
            pady=10,
            font=("Arial", 11),
        ).pack(fill="both", expand=True)

    def _format_zone_info(self, zone) -> str:
        """Return user-facing hover details for one zone."""
        current_count = self.zone_drone_counts.get(zone.name, 0)
        zone_type = getattr(zone.zone_type, "value", str(zone.zone_type))

        return (
            f"Name: {zone.name}\n"
            f"Type: {zone_type}\n"
            f"Coordinates: ({zone.x}, {zone.y})\n"
            f"Colour: {zone.colour or 'lightblue'}\n"
            f"Capacity: {current_count}/{zone.max_drones}"
        )

    def _on_zone_enter(self, zone) -> None:
        """Update sidebar info when mouse hovers a zone."""
        self.zone_info_var.set(self._format_zone_info(zone))

    def _on_zone_leave(self) -> None:
        """Reset sidebar info when mouse leaves a zone."""
        self.zone_info_var.set("Move the mouse over a zone to see details.")

    def _make_zone_enter_handler(self, zone):
        """Create an event handler for zone hover enter."""
        def _handler(_event) -> None:
            self._on_zone_enter(zone)

        return _handler

    def _make_zone_leave_handler(self):
        """Create an event handler for zone hover leave."""
        def _handler(_event) -> None:
            self._on_zone_leave()

        return _handler

    def draw_frame(self) -> None:
        """Clears the canvas and redraws the map and drones for the current turn."""
        # 1. Clear everything
        self.canvas.delete("all")

        # Redraw the turn counter
        self.canvas.create_text(
            50, 20, text=f"Turn: {self.current_step} / {self.max_step}", font=("Arial", 14, "bold"), anchor="w")

        scale, offset_x, offset_y, radius = self._layout()
        drone_radius = max(3, min(6, radius // 2))
        drone_jitter = max(2, min(8, radius // 2))

        current_positions = self.history[self.current_step]
        counts: dict[str, int] = defaultdict(int)
        for zone_name in current_positions.values():
            counts[zone_name] += 1
        self.zone_drone_counts = dict(counts)

        # 2. Draw Connections
        for conn in self.network.connections:
            x1 = int(conn.zone1.x * scale + offset_x)
            y1 = int(conn.zone1.y * scale + offset_y)
            x2 = int(conn.zone2.x * scale + offset_x)
            y2 = int(conn.zone2.y * scale + offset_y)
            self.connect(self.canvas, x1, y1, x2, y2)

        # 3. Draw Zones
        for zone in self.network.zones.values():
            x = int(zone.x * scale + offset_x)
            y = int(zone.y * scale + offset_y)

            color = self._safe_colour(zone.colour, "lightblue")

            if color == "rainbow":
                self._draw_rainbow_zone(x, y, radius)
            else:
                self.canvas.create_oval(
                    x - radius,
                    y - radius,
                    x + radius,
                    y + radius,
                    fill=color,
                )

            hover_zone = self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill="",
                outline="",
            )
            self.canvas.tag_bind(
                hover_zone,
                "<Enter>",
                self._make_zone_enter_handler(zone),
            )
            self.canvas.tag_bind(
                hover_zone,
                "<Leave>",
                self._make_zone_leave_handler(),
            )

        # 4. DRAW DRONES

        for drone_id, zone_name in current_positions.items():
            if zone_name in self.network.zones:
                zone = self.network.zones[zone_name]
                base_x = int(zone.x * scale + offset_x)
                base_y = int(zone.y * scale + offset_y)

                # Add a tiny bit of random scatter so multiple drones don't overlap perfectly
                dx = base_x + random.randint(-drone_jitter, drone_jitter)
                dy = base_y + random.randint(-drone_jitter, drone_jitter)

                # Draw the drone as a small black dot
                self.canvas.create_oval(
                    dx - drone_radius,
                    dy - drone_radius,
                    dx + drone_radius,
                    dy + drone_radius,
                    fill="black",
                )

    def quit(self, event=None) -> None:
        """Close the visualiser window."""
        self.graph.destroy()

    def next_step(self, event=None) -> None:
        """Fires when you press the Right Arrow."""
        if self.current_step < self.max_step:
            self.current_step += 1
            self.draw_frame()

    def prev_step(self, event=None) -> None:
        """Fires when you press the Left Arrow."""
        if self.current_step > 0:
            self.current_step -= 1
            self.draw_frame()
