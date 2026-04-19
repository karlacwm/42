import os
import tkinter as tk
from collections import defaultdict
from tkinter import Canvas


class Visualiser:
    def __init__(self,
                 network,
                 canvas_w: int = 800,
                 canvas_h: int = 600,
                 padding: int = 50,
                 map_filepath: str = "") -> None:
        self.network = network
        self.canvas_w = max(canvas_w, 1800)
        self.total_h = max(canvas_h, 1200)
        self.canvas_h = self.total_h
        self.padding = padding
        self.map_filepath = map_filepath
        self.sidebar_ratio = 0.20
        self.sidebar_min_height = 180

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

        radius = int(max(20, min(30, rough_scale * 0.3)))

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
        x1, y1, x2, y2 = self._shorten_line(x1, y1, x2, y2, 10)
        canvas.create_line(x1, y1, x2, y2, fill="LavenderBlush4", width=2)

    def _shorten_line(self,
                      x1: int,
                      y1: int,
                      x2: int,
                      y2: int,
                      amount: int) -> tuple[int, int, int, int]:
        """Trim a line from both ends by a small amount."""
        dx = x2 - x1
        dy = y2 - y1
        length = (dx * dx + dy * dy) ** 0.5

        if length == 0 or length <= (amount * 2):
            return x1, y1, x2, y2

        shrink_x = (dx / length) * amount
        shrink_y = (dy / length) * amount
        return (
            int(round(x1 + shrink_x)),
            int(round(y1 + shrink_y)),
            int(round(x2 - shrink_x)),
            int(round(y2 - shrink_y)),
        )

    def _safe_colour(self, colour: str, default: str = "lightblue") -> str:
        if not colour or colour.strip().lower() == "rainbow":
            return colour.strip().lower() if colour else default
        try:
            self.canvas.winfo_rgb(colour)
            return colour
        except tk.TclError:
            print(f"Oops. The colour '{colour}' in map config is not on our "
                  f"colour palette. Using default colour '{default}' instead.")
            return default

    def _draw_rainbow_zone(self,
                           x: int,
                           y: int,
                           radius: int) -> None:
        """Draw a zone with rainbow slices."""
        colours = [
            "#E27F7F",
            "#E4A15D",
            "#E2E27B",
            "#76D176",
            "#648BE0",
            "#538366",
            "#6E608F"
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
            outline="#ffffff",
            width=2,
        )

    def visualise(self, history: list) -> None:
        self.history = history
        self.current_step = 0
        self.max_step = len(history) - 1
        self.zone_drone_counts: dict[str, int] = {}
        self.num_drones = len(history[0]) if history else 0
        self._resize_job: str | None = None

        self.graph = tk.Tk()
        self.graph.title("Fly-in Visualiser")

        self.main_frame = tk.Frame(self.graph)
        self.main_frame.pack(fill="both", expand=True)

        self.graph_frame = tk.Frame(self.main_frame, bg="#88bcd1")
        self.graph_frame.pack(side="top", fill="both", expand=True)
        self.graph_frame.pack_propagate(False)

        initial_sidebar_height = self._sidebar_height_for(self.total_h)
        initial_graph_height = max(self.total_h - initial_sidebar_height, 1)
        self.canvas_h = initial_graph_height

        self.canvas = tk.Canvas(
            self.graph_frame,
            width=self.canvas_w,
            height=initial_graph_height,
            bg="#88bcd1",
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(
            self.main_frame,
            height=initial_sidebar_height,
            bg="#91BE90",
            padx=12,
            pady=12,
        )
        self.sidebar.pack(side="bottom", fill="x")
        self.sidebar.pack_propagate(False)

        self._build_sidebar()

        # Key Bindings to move through time!
        self.graph.bind("<Right>", self.next_step)
        self.graph.bind("<Left>", self.prev_step)
        self.graph.bind("<Escape>", self.quit)
        self.graph.bind("<Configure>", self._on_resize)

        # Set window geometry and force layout update
        self.graph.geometry(f"{self.canvas_w}x{self.total_h}")
        self.graph.update_idletasks()

        # Draw the first frame (Turn 0)
        self._apply_layout_resize()
        self.draw_frame()

        self.graph.mainloop()

    def _build_sidebar(self) -> None:
        controls_panel = tk.Frame(self.sidebar, bg="#91BE90")
        controls_panel.pack(side="left", fill="both",
                            expand=True, padx=(0, 18))

        tk.Label(controls_panel, text="Controls", anchor="w", bg="#91BE90",
                 fg="#242335", font=("Arial", 18, "bold")).pack(fill="x",
                                                                pady=(0, 8))
        for line in ["   🢂     Next turn", "   🢀     Previous turn",
                     " ESC   Quit visualiser"]:
            tk.Label(controls_panel, text=line, anchor="w", justify="left",
                     bg="#91BE90", fg="#242335",
                     font=("Arial", 15)).pack(fill="x", pady=2)

        tk.Frame(self.sidebar, bg="#7f9d7e", width=2).pack(
            side="left", fill="y", padx=(0, 18))

        status_panel = tk.Frame(self.sidebar, bg="#91BE90")
        status_panel.pack(side="left", fill="both", expand=True, padx=(0, 18))

        map_name = (os.path.basename(self.map_filepath)
                    if self.map_filepath else "Unknown")
        self.map_name_var = tk.StringVar(value=f"Map: {map_name}")
        self.drone_count_var = tk.StringVar(value=f"Drones: {self.num_drones}")
        self.turn_var = tk.StringVar(
            value=f"Turn: {self.current_step} / {self.max_step}")

        tk.Label(status_panel, text="Map stats", anchor="w", bg="#91BE90",
                 fg="#242335", font=("Arial", 18, "bold")).pack(fill="x",
                                                                pady=(0, 8))
        tk.Label(status_panel, textvariable=self.map_name_var, anchor="w",
                 justify="left", bg="#91BE90", fg="#242335",
                 font=("Arial", 15)).pack(fill="x", pady=2)
        tk.Label(status_panel, textvariable=self.drone_count_var, anchor="w",
                 justify="left", bg="#91BE90", fg="#242335",
                 font=("Arial", 15)).pack(fill="x", pady=2)
        tk.Label(status_panel, textvariable=self.turn_var, anchor="w",
                 justify="left", bg="#91BE90", fg="#242335",
                 font=("Arial", 15)).pack(fill="x", pady=2)

        self.info_panel = tk.Frame(self.sidebar, bg="#91BE90", width=700)
        self.info_panel.pack(side="left", fill="both", expand=False,
                             padx=(0, 12))
        self.info_panel.pack_propagate(False)

        tk.Label(self.info_panel, text="Zone", anchor="w", fg="#242335",
                 bg="#91BE90", font=("Arial", 18, "bold")).pack(fill="x",
                                                                pady=(0, 8))

        self.zone_info_var = tk.StringVar()
        self.zone_info_var.set("Move the mouse over a zone to see details.")

        zone_border = tk.Frame(self.info_panel, bg="#7f9d7e", padx=2, pady=2)
        zone_border.pack(fill="both", expand=True)

        self.zone_info_label = tk.Label(
            zone_border, textvariable=self.zone_info_var, anchor="nw",
            justify="left", wraplength=900, bg="#91BE90", fg="#242335",
            padx=10, pady=10, font=("Arial", 15))
        self.zone_info_label.pack(fill="both", expand=True)

    def _format_zone_info(self, zone) -> str:
        current_count = self.zone_drone_counts.get(zone.name, 0)
        zone_type = getattr(zone.zone_type, "value", str(zone.zone_type))
        return (f"Name: {zone.name}\nType: {zone_type}\n"
                f"Coordinates: ({zone.x}, {zone.y})\n"
                f"Colour: {zone.colour or 'lightblue'}\n"
                f"Capacity: {current_count}/{zone.max_drones}")

    def _on_zone_enter(self, zone) -> None:
        self.zone_info_var.set(self._format_zone_info(zone))

    def _on_zone_leave(self) -> None:
        self.zone_info_var.set("Move the mouse over a zone to see details.")

    def _make_zone_enter_handler(self, zone):
        return lambda _: self._on_zone_enter(zone)

    def _make_zone_leave_handler(self):
        return lambda _: self._on_zone_leave()

    def _on_resize(self, event) -> None:
        """Debounce window resize events and redraw the graph."""
        if self._resize_job is not None:
            self.graph.after_cancel(self._resize_job)

        self._resize_job = self.graph.after(50, self._apply_resize)

    def _apply_resize(self) -> None:
        """Update cached canvas size and redraw after a resize."""
        self._resize_job = None

        new_width = max(self.canvas.winfo_width(), 1)
        new_height = max(self.canvas.winfo_height(), 1)

        if new_width == self.canvas_w and new_height == self.canvas_h:
            return

        self.canvas_w = new_width
        self.canvas_h = new_height
        self._apply_layout_resize()
        self.draw_frame()

    def _sidebar_height_for(self, total_height: int) -> int:
        """Return the sidebar height for a given total window height."""
        return max(
            int(total_height * self.sidebar_ratio),
            self.sidebar_min_height,
        )

    def _apply_layout_resize(self) -> None:
        """Resize graph and sidebar so they share the total window height."""
        if not hasattr(self, "sidebar"):
            return

        window_height = max(self.graph.winfo_height(), self.total_h)
        sidebar_height = self._sidebar_height_for(window_height)
        graph_height = max(window_height - sidebar_height, 1)

        self.canvas_h = graph_height
        self.graph_frame.configure(height=graph_height)
        self.canvas.configure(height=graph_height)
        self.sidebar.configure(height=sidebar_height)

        if hasattr(self, "zone_info_label"):
            sidebar_width = max(self.graph.winfo_width(), self.canvas_w)
            self.zone_info_label.configure(
                wraplength=max(sidebar_width - 420, 300)
            )

    def _zone_spots(self,
                    zone_radius: int,
                    drone_radius: int) -> list[tuple[int, int]]:
        """Return four fixed drone offsets: TL, TR, BL, BR."""
        inset = max(drone_radius + 1, zone_radius // 2)
        return [
            (-inset, -inset),  # top-left
            (inset, -inset),   # top-right
            (-inset, inset),   # bottom-left
            (inset, inset),    # bottom-right
        ]

    def _draw_drone_triangle(self,
                             x: int,
                             y: int,
                             size: int) -> None:
        """Draw one drone as a filled triangle."""
        self.canvas.create_polygon(
            x,
            y - size,
            x - size,
            y + size,
            x + size,
            y + size,
            fill="#4E4683",
            outline="#260DC7",
        )

    def draw_frame(self) -> None:
        """Clears the canvas and redraws the map and drones for the
        current turn."""
        # 1. Clear everything
        self.canvas.delete("all")

        self.turn_var.set(f"Turn: {self.current_step} / {self.max_step}")

        scale, offset_x, offset_y, radius = self._layout()
        drone_radius = max(3, min(6, radius // 2))
        zone_spots = self._zone_spots(radius, drone_radius)

        current_positions = self.history[self.current_step]
        counts: dict[str, int] = defaultdict(int)
        for zone_name in current_positions.values():
            counts[zone_name] += 1
        self.zone_drone_counts = dict(counts)

        drones_by_zone: dict[str, list[str]] = defaultdict(list)
        for drone_id, zone_name in current_positions.items():
            drones_by_zone[zone_name].append(drone_id)

        for zone_name in drones_by_zone:
            drones_by_zone[zone_name].sort()

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
                    outline=""
                )

            hover_zone = self.canvas.create_oval(
                x - radius,
                y - radius,
                x + radius,
                y + radius,
                fill="",
                outline=""
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

        for zone_name, drone_ids in drones_by_zone.items():
            if zone_name not in self.network.zones:
                continue

            zone = self.network.zones[zone_name]
            base_x = int(zone.x * scale + offset_x)
            base_y = int(zone.y * scale + offset_y)

            visible_count = min(len(drone_ids), 4)
            for i in range(visible_count):
                spot_x, spot_y = zone_spots[i]
                dx = base_x + spot_x
                dy = base_y + spot_y

                self._draw_drone_triangle(dx, dy, drone_radius)

            overflow = len(drone_ids) - 4
            if overflow > 0:
                self.canvas.create_text(
                    base_x,
                    base_y,
                    text=f"+{overflow}",
                    fill="white",
                    font=("Arial", 9, "bold"),
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
