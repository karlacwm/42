#!/usr/bin/env python3
"""
Main function or A-Maze-ing project, reading config values from config.txt,
demonstrating maze generation, displaying its visualization
and its user-interactive menu.
"""

import sys
import os
from mazegen import (
    parse_config,
    validate_maze_config,
    generate_maze,
    get_pattern_cells,
    render_unicode,
    render_path_animation,
    find_shortest_path,
    write_output_file
)


valid_colour = {
    'white', 'blue_green', 'brown', 'light_gray',
    'blue', 'marroon', 'forest_green', 'dark_gray',
    'lime', 'navy_blue', 'tan', 'green', 'red',
    'pink', 'rust', 'coffee_brown',
    'black', 'purple', 'dandelion_yellow', 'moon_glow',
    'orange', 'gray', 'highlighter',
    'yellow', 'magenta', 'sky_blue'}

msg = (
    "Choose one from the available colours:\n"
    "|  pink  |    marroon   |       purple     |    magenta  |\n"
    "| yellow |    orange    | dandelion_yellow | highlighter |\n"
    "|  lime  | forest_green |   coffee_brown   |    brown    |\n"
    "|  blue  |  blue_green  |     sky_blue     |  navy_blue  |\n"
    "|  white |     black    |     moon_glow    |     tan     |\n"
    "|  gray  |   dark_gray  |    light_gray    |     rust    |\n"
)

# Add src to path for development
sys.path.insert(0, os.path.join(
    os.path.dirname(__file__), '..', 'mazegen'
))


def update_config(config_file: str, key: str, value: str) -> None:
    """
    Update a configuration value in the config file.
    """
    try:
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

    except IOError as e:
        print(f"Error updating config file: {e}")


def display_menu() -> str:
    """
    Display the main menu and get user choice.
    """
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
    return input("Enter your choice: ").strip()


def change_config_color(config_file: str, key: str, prompt: str) -> None:
    """
    Handle user input for changing a color setting.
    """
    print(f"\n{prompt}\n\n{msg}")

    # range(2) to allow two attempts
    for _ in range(2):
        colour = input("Colour: ").strip().lower()
        if colour in valid_colour:
            update_config(config_file, key, colour)
            print(f"Updated {key} to {colour}!")
            return
        print(f"\nSorry, '{colour}' is not available (¯―¯٥)")

    print("Redirecting you to the menu...\n")


def main() -> None:
    """
    Main function to execute maze generation through parsing config file,
    calling rendering, solver and animation functions, as well as displaying
    user-interactive menu and allowing options for users to navigate it.
    """
    print("=== A_Maze_Ing is amazing ===\n")
    current_maze = None
    current_path = None
    show_path = False
    config = None
    config_file = os.path.join(os.path.dirname(__file__), 'config.txt')

    # FLAG: Only render when something changes
    maze_regen_flag = True
    while True:
        # 1. Generate Maze if needed
        if current_maze is None:
            if not os.path.exists(config_file):
                print(f"Error: Config file not found at {config_file}")
                return

            print("Generating maze from 'config.txt'...")
            try:
                config = parse_config(config_file)
                config = validate_maze_config(config)
            except Exception as e:
                print(f"Critical error caught when parsing config file.\n{e}")
                sys.exit(1)

            forbidden = get_pattern_cells(
                config['width'], config['height'])

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

            try:
                current_maze = generate_maze(
                    width=config['width'],
                    height=config['height'],
                    algorithm=config['algorithm'],
                    seed=config.get('seed'),
                    perfect=perfect,
                    forbidden=forbidden,
                    loops=loop_count
                )
            except Exception as e:
                print(f"Critical error caught during generation.\n{e}")
                sys.exit(1)

            try:
                current_path = find_shortest_path(
                    current_maze,
                    config['entry_x'],
                    config['entry_y'],
                    config['exit_x'],
                    config['exit_y']
                )
            except Exception as e:
                print(f"Critical error caught during solving the maze.\n{e}")
                sys.exit(1)

            write_output_file(
                current_maze,
                (config['entry_x'], config['entry_y']),
                (config['exit_x'], config['exit_y']),
                current_path,
                "output_maze.txt"
            )
            print(
                f"\nMaze ({current_maze.width} x "
                f"{current_maze.height}) "
                f"is generated using {config['algorithm']} "
                f"algorithm:"
            )
            maze_regen_flag = True

        if maze_regen_flag:
            try:
                if show_path and current_path:
                    render_path_animation(current_maze, current_path, config)
                else:
                    speed = 0.001
                    render_unicode(current_maze, speed, config)
                print()
                maze_regen_flag = False
            except Exception as e:
                print(f"Critical error caught during rendering.\n{e}")

        choice = display_menu()
        print("--------------------------------------")

        if choice == '1':
            # Reset maze and regenerate
            current_maze = None
            current_path = None
            show_path = False

        elif choice == '2':
            # Toggle path visibility
            show_path = not show_path
            maze_regen_flag = True
            if show_path:
                print("Showing path solution... ٩(ˊᗜˋ )و\n")
            else:
                print("Hiding path solution... ٩(ˊᗜˋ )و\n")

        elif choice == '3':
            colour = input(
                "\nWhat colour do you want for the maze walls? (´﹃｀)\n\n"
                f"{msg}\nColour: "
            ).strip().lower()
            if colour in valid_colour:
                update_config(config_file, 'wall_colour', colour)
                if config is not None:
                    config['wall_colour'] = colour
                maze_regen_flag = True
            else:
                print("--------------------------------------")
                print(f"\nSorry this colour '{colour}' is not available (¯―¯٥)\n")
                colour = input(f"{msg}\nChoose again: ").strip().lower()
                if colour in valid_colour:
                    update_config(config_file, 'wall_colour', colour)
                    if config is not None:
                        config['wall_colour'] = colour
                    maze_regen_flag = True
                if colour not in valid_colour:
                    print(f"\nSorry this colour '{colour}' is not available (¯―¯٥)\n"
                          "Redirecting you to the menu...\n")
        elif choice == '4':
            colour = input(
                "\nWhat colour do you want for the maze background? (˶˃ ᵕ ˂˶)\n\n"
                f"{msg}\nColour: ").strip().lower()
            if colour in valid_colour:
                update_config(config_file, 'maze_colour', colour)
                if config is not None:
                    config['maze_colour'] = colour
                maze_regen_flag = True
            else:
                print("------------------------------------------------------")
                print(f"\nSorry this colour '{colour}' is not available (¯―¯٥)\n")
                colour = input(f"{msg}\nChoose again: ").strip().lower()
                if colour in valid_colour:
                    update_config(config_file, 'maze_colour', colour)
                    if config is not None:
                        config['maze_colour'] = colour
                    maze_regen_flag = True
                if colour not in valid_colour:
                    print(f"\nSorry this colour '{colour}' is not available (¯―¯٥)\n"
                          "Redirecting you to the menu...\n")
        elif choice == '5':
            print(f"Available colours:\n{', '.join(valid_colour)}")
            colour = input(
                "\nWhat colour do you want for the 42 egg? ᐠ( ᐛ )ᐟ\n\n"
                f"{msg}\nColour: ").strip().lower()
            if colour in valid_colour:
                update_config(config_file, 'egg42', colour)
                if config is not None:
                    config['egg42'] = colour
                maze_regen_flag = True
            else:
                print("------------------------------------------------------")
                print(f"\nSorry this colour '{colour}' is not available (¯―¯٥)\n")
                colour = input(f"{msg}\nChoose again: ").strip().lower()
                if colour in valid_colour:
                    update_config(config_file, 'egg42', colour)
                    if config is not None:
                        config['egg42'] = colour
                    maze_regen_flag = True
                if colour not in valid_colour:
                    print(f"\nSorry this colour '{colour}' is not available (¯―¯٥)\n"
                          "Redirecting you to the menu...\n")
        elif choice == '6':
            print("Climbing the maze wall to exit...")
            print()
            sys.exit(0)
        else:
            print(f"\n'{choice}' is not one of the available options (╥﹏╥). "
                  "Please choose from 1 to 6.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nKeyboard interrupted. Goodbye!")
        sys.exit(0)
