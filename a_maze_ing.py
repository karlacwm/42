#!/usr/bin/env python3
"""Example usage of the mazegen package."""

import sys
import os
from mazegen import (
    parse_config,
    validate_maze_config,
    generate_maze,
    render_unicode,
    render_path_animation,
    find_shortest_path,
    write_output_file
)
from mazegen.render import get_pattern_cells

# Add src to path for development
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', 'mazegen'
))

# Global state for maze and path
CURRENT_MAZE = None
CURRENT_PATH = None
SHOW_PATH = False


def update_config(config_file: str, key: str, value: str) -> None:
    """Update a configuration value in the config file."""
    with open(config_file, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if (line.strip().startswith(key + ' ') or
                line.strip().startswith(key + '=')):
            lines[i] = f"{key} = {value}\n"
            break
    else:
        lines.append(f"{key} = {value}\n")

    with open(config_file, 'w') as file:
        file.writelines(lines)


def display_menu() -> str:
    print("--------------------------------------")
    print("============ A-Maze-ing ==============")
    print("--------------------------------------")
    print("| 1 | regenerate a maze               |")
    print("| 2 | show/hide path solution         |")
    print("| 3 | change colour - maze wall       |")
    print("| 4 | change colour - maze background |")
    print("| 5 | change colour - 42              |")
    print("| 6 | exit                            |")
    print("--------------------------------------")
    return input("Enter your choice: ")


def main() -> None:
    """Main demo function."""
    global CURRENT_MAZE, CURRENT_PATH, SHOW_PATH

    print("=== A_Maze_Ing is amazing ===\n")

    # Example 1: Generate from config file
    config_file = os.path.join(
        os.path.dirname(__file__), 'config.txt'
    )

    if os.path.exists(config_file):
        print(
            "Getting maze generation request from "
            "the 'config.txt' file..."
        )
        config = parse_config(config_file)
        validate_maze_config(config)
        print(f"Request is parsed as follows:\n{config}")

        # Generate or reuse existing maze
        if CURRENT_MAZE is None:
            # Get the forbidden cells (42 pattern)
            forbidden = get_pattern_cells(
                config['width'], config['height']
            )

            # Calculate loop count based on maze size if not perfect
            perfect = config.get('perfect', True)
            if isinstance(perfect, str):
                perfect = perfect.lower() == 'true'

            loop_count = 0
            if not perfect:
                # Default: 10% of cells as number of loops
                loop_count = max(1, (
                    config['width'] * config['height'] // 10
                ))

            CURRENT_MAZE = generate_maze(
                width=config['width'],
                height=config['height'],
                algorithm=config['algorithm'],
                seed=config.get('seed'),
                perfect=perfect,
                forbidden=forbidden,
                loops=loop_count
            )
            # Calculate path for the new maze
            CURRENT_PATH = find_shortest_path(
                CURRENT_MAZE,
                config['entry_x'],
                config['entry_y'],
                config['exit_x'],
                config['exit_y']
            )
        write_output_file(
            CURRENT_MAZE,
            (config['entry_x'], config['entry_y']),
            (config['exit_x'], config['exit_y']),
            CURRENT_PATH,
            "output_maze.txt"
        )
        speed = 0.001
        print(
            f"\nMaze ({CURRENT_MAZE.width} x "
            f"{CURRENT_MAZE.height}) "
            f"is generated using {config['algorithm']} "
            f"algorithm:"
        )

        # Render with or without path
        if SHOW_PATH and CURRENT_PATH:
            print("(Path is shown)\n")
            render_path_animation(
                CURRENT_MAZE, CURRENT_PATH
            )
        else:
            render_unicode(CURRENT_MAZE, speed)
        print()

    while True:
        choice = display_menu().strip()
        print("--------------------------------------")

        valid_color = {
            'blue', 'marroon', 'forest_green', 'dark_gray', 'pink',
            'coffee_brown', 'black', 'purple', 'dandilion_yellow',
            'moon_glow', 'orange', 'gray', 'highlighter',
            'yellow', 'magenta', 'sky_blue'}
        msg = (
            "Choose one from the available colours:\n"
            "black       |  marroon   |  sky_blue  |  light_gray\n"
            "moon_glow   |  gray      |  purple    |  dark_gray\n"
            "yellow      |  orange    |  magenta   |  dandilion_yellow\n"
            "highlighter |  pink      |  blue      |  coffee_brown\n"
            )

        if choice not in ('1', '2', '3', '4', '5', '6'):
            print(f"\n'{choice}' is not one of the available options (╥﹏╥). "
                  "Please choose from 1 to 6.\n")
            continue
        if choice == '1':
            # Reset maze and regenerate
            CURRENT_MAZE = None
            CURRENT_PATH = None
            SHOW_PATH = False
            main()
        elif choice == '2':
            # Toggle path visibility
            SHOW_PATH = not SHOW_PATH
            if SHOW_PATH:
                print("Showing path solution... ٩(ˊᗜˋ )و\n")
            else:
                print("Hiding path solution... (ദ്ദി˙ᗜ˙)\n")
            main()
        elif choice == '3':
            color = input(
                "\nWhat colour do you want for the maze walls? (´﹃｀)\n\n"
                f"{msg}\nColour: "
            ).strip().lower()
            if color in valid_color:
                update_config(config_file, 'wall_color', color)
                main()
            else:
                print("--------------------------------------")
                print(f"\nSorry this colour '{color}' is not available (¯―¯٥)\n")
                color = input(f"{msg}\nChoose again: ").strip().lower()
                if color not in valid_color:
                    print(f"\nSorry this colour '{color}' is not available (¯―¯٥)\n"
                          "Redirecting you to the menu...\n")
        elif choice == '4':
            color = input(
                "\nWhat colour do you want for the maze background? (˶˃ ᵕ ˂˶)\n\n"
                f"{msg}\nColour: "
            ).strip().lower()
            if color in valid_color:
                update_config(config_file, 'maze_color', color)
                main()
            else:
                print("------------------------------------------------------")
                print(f"\nSorry this colour '{color}' is not available (¯―¯٥)\n")
                color = input(f"{msg}\nChoose again: ").strip().lower()
                if color not in valid_color:
                    print(f"\nSorry this colour '{color}' is not available (¯―¯٥)\n"
                          "Redirecting you to the menu...\n")
        elif choice == '5':
            print(f"Available colours:\n{', '.join(valid_color)}")
            color = input(
                "\nWhat colour do you want for the 42 egg? ᐠ( ᐛ )ᐟ\n\n"
                f"{msg}\nColour: "
            ).strip().lower()
            if color in valid_color:
                update_config(config_file, 'egg42', color)
                main()
            else:
                print("------------------------------------------------------")
                print(f"\nSorry this colour '{color}' is not available (¯―¯٥)\n")
                color = input(f"{msg}\nChoose again: ").strip().lower()
                if color not in valid_color:
                    print(f"\nSorry this colour '{color}' is not available (¯―¯٥)\n"
                          "Redirecting you to the menu...\n")
        elif choice == '6':
            print("Climbing the maze wall to exit...")
            print()
            sys.exit(0)


if __name__ == '__main__':
    main()
