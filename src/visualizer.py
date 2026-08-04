import sys
import subprocess


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

        subprocess.run(["clear"], check=False)
        sys.stdout.write(
            "               "
            f"(ㅅ´ ˘ `) Received a total of {self.total} calls to make ~ \n\n"
            "                              "
            f"Making call #{self.current}...\n"
            f"and here's a progress bar to entertain us: [{bar}] {percent}%\n"
        )
        sys.stdout.flush()

    def finish(self) -> None:
        sys.stdout.write("\n")
        sys.stdout.flush()

    @staticmethod
    def print_done(filepath: str) -> None:
        """Shows that the program finishes."""
        subprocess.run(["clear"], check=False)
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
           "                                              "
           "      ✩    ⋆✮"
           f"\n\n   Check the results now in {filepath}"
           "\n                (◍•ᴗ•◍)✧*。 Call again soon! 。*✧(◍•ᴗ•◍)\n")
