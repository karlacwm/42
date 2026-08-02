import sys


class Visualizer:
    """Displays progress bars and status updates in the terminal."""

    @staticmethod
    def print_start() -> None:
        """Shows that the program starts."""
        print("\n( ˶°ㅁ°)* ✧ﾟ･✧ Loading prompts and "
              "calling functions ✧ﾟ･✧ *(°ㅁ°˶ )\n")

    @staticmethod
    def show_progress(current: int, total: int,
                      prefix: str = "Processing") -> None:
        """Draws a progress bar in terminal"""
        bar_length = 30
        progress = current / total if total > 0 else 1.0
        filled_length = int(bar_length * progress)

        # Create filled '█' and empty '░' blocks
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        percent = int(progress * 100)

        # '\r' moves cursor back to  start of line so it updates in-place
        sys.stdout.write(f"\r{prefix}: [{bar}] {percent}% ({current}/{total})")
        sys.stdout.flush()
        if current == total:
            print()  # Print a newline when finished

    @staticmethod
    def print_done() -> None:
        """Shows that the program finishes."""
        print("\n(◍•ᴗ•◍)✧*。 All Done! Check the output! 。*✧(◍•ᴗ•◍)\n")
