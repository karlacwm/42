import sys


def ft_command_quest() -> None:
    argv_count: int = len(sys.argv)
    print("=== Command Quest ===")
    print("Program name:", sys.argv[0])
    if argv_count > 1:
        print("Arguments received:", argv_count - 1)
    else:
        print("No arguments provided!")
    for i in range(1, argv_count):
        print(f"Argument {i}:", sys.argv[i], end="\n")
    print("Total arguments:", argv_count)


if __name__ == "__main__":
    ft_command_quest()
