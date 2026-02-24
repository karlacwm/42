#!/usr/bin/env python3
"""Example usage of the mazegen package."""

import sys
import os

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from mazegen import (  # noqa: E402
    parse_config, validate_maze_config, generate_maze,
    render_ascii, render_ascii_compact, render_mlx_detailed
)


def main() -> None:
    """Main demo function."""
    print("=== A_Maze_Ing Maze Generator Demo ===\n")

    # Example 1: Generate from config file
    config_file = os.path.join(os.path.dirname(__file__), 'maze_config.txt')

    if os.path.exists(config_file):
        print("Example 1: Loading from config file")
        config = parse_config(config_file)
        print(f"Config: {config}")
        validate_maze_config(config)

        maze = generate_maze(
            width=config['width'],
            height=config['height'],
            algorithm=config['algorithm'],
            seed=config.get('seed')
        )

        print(f"\nGenerated {config['algorithm']} maze ({maze.width}x{maze.height}):")
        print(render_ascii(maze))
        print()

    # Example 2: Generate programmatically with Prim's algorithm
    print("Example 2: Prim's algorithm (5x5)")
    maze_prim = generate_maze(5, 5, algorithm='prim', seed=42)
    print(render_ascii_compact(maze_prim))
    print()

    # Example 3: Generate with Kruskal's algorithm
    print("Example 3: Kruskal's algorithm (5x5)")
    maze_kruskal = generate_maze(5, 5, algorithm='kruskal', seed=42)
    print(render_ascii_compact(maze_kruskal))
    print()

    # Example 4: MLX format (hex encoding)
    print("Example 4: MLX format (hex wall encoding)")
    small_maze = generate_maze(4, 3, algorithm='prim', seed=123)
    print(render_mlx_detailed(small_maze))
    print()

    print("Wall encoding: N=0x1, E=0x2, S=0x4, W=0x8")
    print("For example, 0xF means all walls, 0x0 means no walls")


if __name__ == '__main__':
    main()
