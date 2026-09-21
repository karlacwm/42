import sys


def ft_command_quest() -> None:
    '''
    Shows details about the arguments received from terminal.
    '''
    argv_count: int = len(sys.argv)
    print("=== Command Quest ===")
    if argv_count == 1:
        print("No arguments provided!")
    print("Program name:", sys.argv[0])
    if argv_count > 1:
        print("Arguments received:", argv_count - 1)
    i = 1
    for arg in sys.argv[1:]:
        print(f"Argument {i}:", arg)
        i += 1
    print("Total arguments:", argv_count)


if __name__ == "__main__":
    ft_command_quest()
