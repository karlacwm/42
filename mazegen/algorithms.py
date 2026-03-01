import random
from typing import Tuple, Set, List
from .maze import Maze
from .class_maze_generator import MazeGenerator


class PrimGenerator(MazeGenerator):
    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)
        protected = self.get_protected_cells()

        # Start at random point (avoiding protected cells)
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        while (start_x, start_y) in protected:
            start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)

        visited: Set[Tuple[int, int]] = {(start_x, start_y)} | protected
        walls = []

        # Add initial walls
        for nx, ny, _ in maze.get_neighbors(start_x, start_y):
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

        for y in range(self.height):
            for x in range(self.width):
                # East wall
                if x < self.width - 1:
                    if (x, y) not in protected and (x+1, y) not in protected:
                        edges.append((x, y, x + 1, y))
                # South wall
                if y < self.height - 1:
                    if (x, y) not in protected and (x, y+1) not in protected:
                        edges.append((x, y, x, y + 1))

        random.shuffle(edges)
        uf = self.UnionFind(self.width * self.height)

        for x1, y1, x2, y2 in edges:
            idx1 = y1 * self.width + x1
            idx2 = y2 * self.width + x2
            if uf.union(idx1, idx2):
                maze.remove_wall_between(x1, y1, x2, y2)
        return maze


class BacktrackingGenerator(MazeGenerator):
    def generate(self) -> Maze:
        maze = Maze(self.width, self.height)
        protected = self.get_protected_cells()

        visited: Set[Tuple[int, int]] = protected.copy()
        stack: List[Tuple[int, int]] = []

        # Start with a random cell
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)

        while (start_x, start_y) in protected:
            start_x = random.randint(0, self.width - 1)
            start_y = random.randint(0, self.height - 1)

        stack.append((start_x, start_y))
        visited.add((start_x, start_y))

        # Main loop: process cells from the stack
        while stack:
            current_x, current_y = stack[-1]

            # Get all unvisited neighbors
            unvisited_neighbors = [
                (nx, ny, direction)
                for nx, ny, direction in maze.get_neighbors(current_x, current_y)
                if (nx, ny) not in visited
            ]

            if not unvisited_neighbors:
                # No unvisited neighbors, backtrack
                stack.pop()
            else:
                # Choose a random unvisited neighbor
                next_x, next_y, direction = random.choice(unvisited_neighbors)

                # Remove wall between current and next cell
                maze.remove_wall_between(current_x, current_y, next_x, next_y)

                # Mark next cell as visited and push to stack
                visited.add((next_x, next_y))
                stack.append((next_x, next_y))
        return maze
