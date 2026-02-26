#!/usr/bin/env python3
"""Example usage of the mazegen package."""

import sys
import os
from src.mazegen import parse_config, generate_maze, render_unicode

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def update_config(config_file: str, key: str, value: str) -> None:
    """Update a configuration value in the config file."""
    with open(config_file, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith(key + ' ') or line.strip().startswith(key + '='):
            lines[i] = f"{key} = {value}\n"
            break
    else:
        lines.append(f"{key} = {value}\n")

    with open(config_file, 'w') as file:
        file.writelines(lines)


def main() -> None:
    """Main demo function."""
    print("=== A_Maze_Ing is amazing ===\n")

    # Example 1: Generate from config file
    config_file = os.path.join(os.path.dirname(__file__), 'config.txt')

    if os.path.exists(config_file):
        print("Getting maze generation request from the 'config.txt' file...")
        config = parse_config(config_file)
        print(f"Request is parsed as follows:\n{config}")

        maze = generate_maze(
            width=config['width'],
            height=config['height'],
            algorithm=config['algorithm'],
            seed=config.get('seed')
        )
        speed = 0.001
        print(f"\nMaze ({maze.width} x {maze.height}) is generated using {config['algorithm']} algorithm:")
        render_unicode(maze, speed)
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

    valid_color = {'white', 'blue_green', 'brown', 'light_gray',
                        'blue', 'marroon', 'forest_green', 'dark_gray',
                        'green', 'lime', 'navy_blue', 'tan',
                        'red', 'pink', 'rust', 'coffee_brown',
                        'black', 'purple', 'dandilion_yellow', 'moon_glow',
                        'orange', 'gray', 'highlighter',
                        'yellow', 'magenta', 'sky_blue'}

    if choice == '1':
        main()
        # print("Regenerating maze...")
        # config = parse_config(config_file)
        # maze = generate_maze(
        #     width=config['width'],
        #     height=config['height'],
        #     algorithm=config['algorithm'],
        #     seed=config.get('seed')
        # )
        # print(f"\nGenerated {config['algorithm']} maze ({maze.width}x{maze.height}):")
        # render_unicode_animated(maze, speed)
    elif choice == '2':
        print("Toggling path solution...")
        # Here we would toggle the path solution visibility
    elif choice == '3':
        print(f"Available colours: {', '.join(valid_color)}")
        color = input("What colour do you want for the 42 egg?\n").strip().lower()
        if color in valid_color:
            update_config(config_file, 'egg42', color)
            main()
        else:
            print(f"Sorry this colour '{color}' is not available :(")
            print(f"Choose one from the available colours: {', '.join(valid_color)}")
            # or go back to menu?
    elif choice == '4':
        print("Changing maze wall colour...")
        # Here we would change the maze wall colour in the rendering
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
