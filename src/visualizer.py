import sys
import time


class Visualizer:
    """Displays progress bars and status updates in the terminal."""

    message = ["Generating output", "Picking functions", "Working on it",
               "Comparing functions", "Reading prompts", "Calling functions",
               "Updating progress", "Gathering results"]

    @staticmethod
    def print_start() -> None:
        """Shows that the program starts."""
        print("\n                      ~~  Call Me Maybe ~~")
        print("\n( ˶°ㅁ°)* ✧ﾟ･✧ Loading prompts and "
              "calling functions ✧ﾟ･✧ *(°ㅁ°˶ )\n")
        time.sleep(2)

    @staticmethod
    def show_progress(current: int, total: int) -> None:
        sys.stdout.flush()
        bar_length = 30
        progress = current / total if total > 0 else 1.0
        filled_length = int(bar_length * progress)

        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percent = int(progress * 100)

        sys.stdout.write(
            f"\r\033[K Generating output: "
            f"[{bar}] {percent}% ({current}/{total})"
        )
        sys.stdout.flush()

        if current == total:
            print()

    @staticmethod
    def print_done() -> None:
        """Shows that the program finishes."""
        print("\n(◍•ᴗ•◍)✧*。 All Done! Check the output! 。*✧(◍•ᴗ•◍)\n")
