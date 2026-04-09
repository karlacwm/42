import tkinter as tk
from tkinter import font
from network import Network


class Visualizer:
    def __init__(self,
                 network: Network,
                 filepath: str,
                 canvas_width: int = 800,
                 canvas_height: int = 600) -> None:
        self.network = network
        self.filepath = filepath
        self.c_width = canvas_width
        self.c_height = canvas_height

        # UI State
        self.current_step = 0
        # Adjusted to match your parser variable
        self.total_drones = getattr(network, 'drones_total', 0)

        # Colors (Dark Theme)
        self.bg_color = "#2E3440"
        self.panel_color = "#3B4252"
        self.text_color = "#ECEFF4"
        self.line_color = "#4C566A"
        self.node_radius = 18

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Builds the window, sidebar, canvas, AND initializes bindings."""
        self.root = tk.Tk()
        self.root.title("Fly-in Simulation")
        self.root.configure(bg=self.bg_color)
        self.root.geometry(f"{self.c_width + 250}x{self.c_height}")

        # Custom Fonts
        self.title_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.norm_font = font.Font(family="Helvetica", size=11)

        # --- Right Sidebar (Info Panel) ---
        self.sidebar = tk.Frame(self.root, width=250,
                                bg=self.panel_color, relief="flat")
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(self.sidebar,
                 text="SIMULATION DASHBOARD",
                 font=self.title_font,
                 bg=self.panel_color, fg="#88C0D0").pack(pady=(20, 10))
        tk.Label(self.sidebar,
                 text=f"Map File: {self.filepath}",
                 font=self.norm_font,
                 bg=self.panel_color,
                 fg=self.text_color).pack(anchor="w", padx=10, pady=5)
        tk.Label(self.sidebar,
                 text=f"Total Drones: {self.total_drones}",
                 font=self.norm_font,
                 bg=self.panel_color,
                 fg=self.text_color).pack(anchor="w", padx=10, pady=5)

        self.step_label = tk.Label(
            self.sidebar,
            text=f"Current Step: {self.current_step}",
            font=self.title_font,
            bg=self.panel_color,
            fg="#A3BE8C")
        self.step_label.pack(anchor="w",
                             padx=10,
                             pady=20)

        # --- Left Canvas (Network) ---
        self.canvas = tk.Canvas(self.root,
                                width=self.c_width,
                                height=self.c_height,
                                bg=self.bg_color,
                                highlightthickness=0)
        self.canvas.pack(side=tk.LEFT,
                         fill=tk.BOTH,
                         expand=True,
                         padx=20,
                         pady=20)

        # --- Key Bindings ---
        self.root.bind("<Right>", self.next_step)
        self.root.bind("<Left>", self.prev_step)

        # --- Mouse Bindings ---
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<Button-4>", self.zoom)
        self.canvas.bind("<Button-5>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)

    def _get_transform(self):
        """Calculates scale and offset to perfectly center the graph."""
        if not self.network.zones:
            return 1, 0, 0

        xs = [z.x for z in self.network.zones.values()]
        ys = [z.y for z in self.network.zones.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        graph_width = max_x - min_x
        graph_height = max_y - min_y

        padding = 60
        usable_w = self.c_width - (padding * 2)
        usable_h = self.c_height - (padding * 2)

        scale_x = usable_w / graph_width if graph_width > 0 else 1
        scale_y = usable_h / graph_height if graph_height > 0 else 1
        scale = min(scale_x, scale_y)

        offset_x = (self.c_width - (graph_width * scale)) / 2 - (min_x * scale)
        offset_y = (self.c_height - (graph_height * scale)) / \
            2 - (min_y * scale)

        return scale, offset_x, offset_y

    def draw(self) -> None:
        """Draws the network centered on the canvas."""
        self.canvas.delete("all")
        scale, offset_x, offset_y = self._get_transform()

        # 1. Draw Connections
        for conn in self.network.connections:
            x1 = (conn.zone1.x * scale) + offset_x
            y1 = (conn.zone1.y * scale) + offset_y
            x2 = (conn.zone2.x * scale) + offset_x
            y2 = (conn.zone2.y * scale) + offset_y

            self.canvas.create_line(
                x1, y1, x2, y2, width=2, fill=self.line_color)

            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            self.canvas.create_text(
                mid_x, mid_y - 10,
                text=f"Cap: {conn.max_link_capacity}",
                fill="#81A1C1",
                font=("Helvetica", 9))

        # 2. Draw Zones
        for zone in self.network.zones.values():
            cx = (zone.x * scale) + offset_x
            cy = (zone.y * scale) + offset_y

            node_color = zone.colour if zone.colour else "#88C0D0"

            self.canvas.create_oval(
                cx - self.node_radius, cy - self.node_radius,
                cx + self.node_radius, cy + self.node_radius,
                fill=node_color, outline=self.text_color, width=2
            )

            self.canvas.create_text(
                cx, cy - 28, text=zone.name,
                fill=self.text_color,
                font=("Helvetica", 10, "bold"))
            self.canvas.create_text(
                cx, cy + 28,
                text=f"Max: {zone.max_drones}",
                fill="#EBCB8B",
                font=("Helvetica", 9))

    # --- Interaction Methods ---
    def start_pan(self, event) -> None:
        self.canvas.scan_mark(event.x, event.y)

    def pan(self, event) -> None:
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event) -> None:
        if event.num == 4 or getattr(event, 'delta', 0) > 0:
            scale_factor = 1.1
        elif event.num == 5 or getattr(event, 'delta', 0) < 0:
            scale_factor = 0.9
        else:
            return
        self.canvas.scale("all", event.x, event.y, scale_factor, scale_factor)

    def next_step(self, event=None) -> None:
        self.current_step += 1
        self.update_step_ui()
        # TODO: Ask Simulation Engine for drone positions, redraw

    def prev_step(self, event=None) -> None:
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_ui()
            # TODO: Ask Simulation Engine for previous drone positions, redraw

    def update_step_ui(self) -> None:
        self.step_label.config(text=f"Current Step: {self.current_step}")
        self.root.update()

    def run(self) -> None:
        self.draw()
        self.root.mainloop()
