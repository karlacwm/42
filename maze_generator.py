class MazeGenerator():
    def __init__ (self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed

        if seed is not None:
            random.seed(seed)
        
        self.grid = [[15 for _ in range(width)] for _ in range(height)]


class PrimsAlgorithm(MazeGenerator):
    def __init__(self, width: int, height: int, seed: int = None) -> None:
        super().__init__(width, height, seed)

    def generate(self):
        # logic starts here



