import sys
# sys module provides access to Python interpreter internals
import os
# os module interacts with the operating system
import site
# site module manages Python package locations
# also where the pip installs libraries


def check_environment() -> None:
    # global: /usr/bin/python3 (sys.prefix = /usr)
    # virtual: /home/user/project/venv (sys.prefix = /home/user/project/venv)
    # sys.base_prefix still points to /usr in virtual environment
    if sys.prefix != sys.base_prefix:
        in_venv = True
    else:
        in_venv = False

    if not in_venv:
        print("MATRIX STATUS: You're still plugged in")
        print()

        # sys.executable: path to the Python interpreter running the script
        # linux: /usr/bin/python3
        # venv: /home/user/project/venv/bin/python3
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()

        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()

        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\nScripts\nactivate   # On Windows")
        print()

        print("Then run this program again.")
    else:
        print("MATRIX STATUS: Welcome to the construct")
        print()

        print(f"Current Python: {sys.executable}")
        # os.environ: dictionary of environment variables from os
        # access an item: os.environ["HOME"] OR os.environ.get("HOME")
        venv_path = os.environ.get("VIRTUAL_ENV", sys.prefix)
        # os.path.basename grabs just the folder name from the full path
        venv_name = os.path.basename(venv_path)
        print(f"Virtual Environment: {venv_name}")
        print(f"Environment Path: {venv_path}")
        print()

        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()

        print("Package installation path:")
        # Get the path where packages are installed
        # site.getsitepackages() returns a list of paths
        # the first one is usually the local one
        print(site.getsitepackages()[0])


if __name__ == "__main__":
    check_environment()
