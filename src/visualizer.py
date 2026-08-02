import sys


class Visualizer:
    """Displays progress bars and status updates in the terminal."""

    @staticmethod
    def print_header(title: str) -> None:
        """Prints a styled section header."""
        print("\n==================================================")
        print(f"  {title}")
        print("==================================================")

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
