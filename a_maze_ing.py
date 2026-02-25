#!/usr/bin/env python3
"""Example usage of the mazegen package."""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.mazegen import (
    parse_config, validate_maze_config, generate_maze,
    render_unicode_animated)


def main() -> None:
    """Main demo function."""
    print("=== A_Maze_Ing Maze Generator Demo ===\n")

    # Example 1: Generate from config file
    config_file = os.path.join(os.path.dirname(__file__), 'config.txt')

    if os.path.exists(config_file):
        print("Example 1: Loading from config file")
        config = parse_config(config_file)
        print(f"Config: {config}")


        maze = generate_maze(
            width=config['width'],
            height=config['height'],
            algorithm=config['algorithm'],
            seed=config.get('seed')
        )

        print(f"\nGenerated {config['algorithm']} maze ({maze.width}x{maze.height}):")
        render_unicode_animated(maze, 0.05)
        print()

    print("=== A-Maze-ing ===")
    print("1. regenerate a maze")
    print("2. show/hide path solution")
    print("3. change backgroud colour")
    print("4. change maze_wall colour")
    print("5. exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        print("Regenerating maze...")
        config = parse_config(config_file)
        maze = generate_maze(
            width=config['width'],
            height=config['height'],
            algorithm=config['algorithm'],
            seed=config.get('seed')
        )
        print(f"\nGenerated {config['algorithm']} maze ({maze.width}x{maze.height}):")
        render_unicode_animated(maze, 0.05)
        print()
    elif choice == '2':
        print("Toggling path solution...")
        # Here we would toggle the path solution visibility
    elif choice == '3':
        print("Changing background colour...")
        # Here we would change the background colour in the rendering
    elif choice == '4':
        print("Changing maze wall colour...")
        # Here we would change the maze wall colour in the rendering
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)

if __name__ == '__main__':
    main()
