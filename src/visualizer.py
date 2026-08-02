import sys
import os


class Visualizer:
    """Displays progress bars and status updates in the terminal."""

    def __init__(self, total: int) -> None:
        self.total = total
        self.current = 0

    @staticmethod
    def print_start() -> None:
        """Shows that the program starts."""
        print("\n                      ~~  Call Me Maybe ~~")
        print("\n( ˶°ㅁ°)* ✧ﾟ･✧ Loading prompts and "
              "calling functions ✧ﾟ･✧ *(°ㅁ°˶ )\n\n\n")

    def update(self, step: int = 1) -> None:
        self.current += step
        total = max(self.total, 1)
        progress = self.current / total
        bar_length = 30
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)
        percent = int(progress * 100)

        os.system('clear')
        sys.stdout.write(
            f"Generating output: [{bar}] {percent}% "
            f"({self.current}/{self.total})"
        )
        sys.stdout.flush()

    def finish(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def print_done(filepath: str) -> None:
        """Shows that the program finishes."""
        print(
           "\n┊ ✩  ┊   ✧   ┊   ┊"
           "                                    "
           "┊   ┊   ✧   ┊  ✩ ┊"
           "\n┊    ┊★      ┊   ✩⋆"
           "                                  "
           "⋆✩   ┊      ★┊    ┊"
           "\n┊    ┊       ⊹˚"
           "                                          "
           "˚⊹       ┊    ┊"
           "\n✩⋆    ✮      "
           "                                               "
           "      ✩    ⋆✮"
           f"\n\n   Check the results now in {filepath}"
           "\n                (◍•ᴗ•◍)✧*。 Call again soon! 。*✧(◍•ᴗ•◍)\n")
