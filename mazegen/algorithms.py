import random
from typing import Tuple, Set
from .maze import Maze
from .class_maze_generator import MazeGenerator


# --- PRIM'S ALGORITHM ---
class PrimGenerator(MazeGenerator):
    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)

        # Get the '42' protection from the parent class
        protected = self.get_protected_cells()

        # Start at random point (avoiding protected cells)
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        while (start_x, start_y) in protected:
            start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

        visited: Set[Tuple[int, int]] = {(start_x, start_y)} | protected
        walls = []

        # Add initial walls
        for nx, ny, direction in maze.get_neighbors(start_x, start_y):
            walls.append((start_x, start_y, nx, ny))

        while walls:
            idx = random.randint(0, len(walls) - 1)
            x1, y1, x2, y2 = walls.pop(idx)

            if (x2, y2) not in visited:
                maze.remove_wall_between(x1, y1, x2, y2)
                visited.add((x2, y2))
                for nx, ny, _ in maze.get_neighbors(x2, y2):
                    if (nx, ny) not in visited:
                        walls.append((x2, y2, nx, ny))
        return maze


# --- KRUSKAL'S ALGORITHM ---
class KruskalGenerator(MazeGenerator):
    class UnionFind:
        def __init__(self, size: int) -> None:
            self.parent = list(range(size))
            self.rank = [0] * size

        def find(self, x: int) -> int:
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x: int, y: int) -> bool:
            root_x, root_y = self.find(x), self.find(y)
            if root_x == root_y:
                return False
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            return True

    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)
        protected = self.get_protected_cells()
        edges = []

        # Collect all valid edges (skipping protected ones)
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1:
                    if (x, y) not in protected and (x+1, y) not in protected:
                        edges.append((x, y, x+1, y))
                if y < self.height - 1:
                    if (x, y) not in protected and (x, y+1) not in protected:
                        edges.append((x, y, x, y+1))

        random.shuffle(edges)
        uf = self.UnionFind(self.width * self.height)

        for x1, y1, x2, y2 in edges:
            idx1, idx2 = y1 * self.width + x1, y2 * self.width + x2
            if uf.union(idx1, idx2):
                maze.remove_wall_between(x1, y1, x2, y2)

        return maze


# --- BACKTRACKING ALGORITHM ---
class BacktrackingGenerator(MazeGenerator):
    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)
        # Note: Backtracking usually ignores 'protected' or needs complex logic to support it.
        # For now, we run standard backtracking.

        stack = []
        visited = set()

        start_x, start_y = random.randint(0, self.width-1), random.randint(0, self.height-1)
        stack.append((start_x, start_y))
        visited.add((start_x, start_y))

        while stack:
            cx, cy = stack[-1]
            neighbors = []
            for nx, ny, _ in maze.get_neighbors(cx, cy):
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny))

            if neighbors:
                nx, ny = random.choice(neighbors)
                maze.remove_wall_between(cx, cy, nx, ny)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        return maze
