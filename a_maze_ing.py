#!/usr/bin/env python3
"""Example usage of the mazegen package."""

import sys
import os
from src.mazegen import (
    parse_config,
    generate_maze,
    render_unicode,
    render_unicode_with_path,
    find_shortest_path
)

# Add src to path for development
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', 'src'
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
        print(f"Request is parsed as follows:\n{config}")

        # Generate or reuse existing maze
        if CURRENT_MAZE is None:
            CURRENT_MAZE = generate_maze(
                width=config['width'],
                height=config['height'],
                algorithm=config['algorithm'],
                seed=config.get('seed')
            )
            # Calculate path for the new maze
            CURRENT_PATH = find_shortest_path(
                CURRENT_MAZE,
                config['entry_x'],
                config['entry_y'],
                config['exit_x'],
                config['exit_y']
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
            render_unicode_with_path(
                CURRENT_MAZE, CURRENT_PATH, speed
            )
        else:
            render_unicode(CURRENT_MAZE, speed)
        print()

    print("--------------------------------------")
    print("============ A-Maze-ing ==============")
    print("--------------------------------------")
    print("| 1 | regenerate a maze               |")
    print("| 2 | show/hide path solution         |")
    print("| 3 | change 42 colour                |")
    print("| 4 | change maze_wall colour         |")
    print("| 5 | exit                            |")
    print("--------------------------------------")
    choice = input("Enter your choice: ")
    valid_color = {
        'blue', 'marroon', 'forest_green', 'dark_gray',
        'coffee_brown', 'black', 'purple', 'dandelion_yellow',
        'moon_glow', 'orange', 'gray', 'highlighter',
        'yellow', 'magenta', 'sky_blue'}

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
            print("Showing path solution...\n")
        else:
            print("Hiding path solution...\n")
        main()
    elif choice == '3':
        print(f"Available colours:\n{', '.join(valid_color)}")
        color = input(
            "What colour do you want for the 42 egg?\n"
        ).strip().lower()
        if color in valid_color:
            update_config(config_file, 'egg42', color)
            main()
        else:
            print(f"Sorry this colour '{color}' is not available :(")
            msg = (f"Choose one from the available colours:\n"
                   f"{', '.join(valid_color)}")
            print(msg)
            # or go back to menu?
    elif choice == '4':
        print(f"Available colours:\n{', '.join(valid_color)}")
        color = input(
            "What colour do you want for the maze walls?\n"
        ).strip().lower()
        if color in valid_color:
            update_config(config_file, 'wall_color', color)
            main()
        else:
            print(f"Sorry this colour '{color}' is not available :(")
            msg = (f"Choose one from the available colours:\n"
                   f"{', '.join(valid_color)}")
            print(msg)
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
