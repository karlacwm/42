import sys


def loading() -> None:
    if sys.prefix != sys.base_prefix:
        in_venv = True
    else:
        in_venv = False
    if not in_venv:
        print("ERROR: You're not in a virtual environment!")
        print("Please create one or activate it before you try again.")
        print("To create one: 'python3 -m venv matrix_env'")
        print("To activate it: 'source matrix_env/bin/activate'")
        sys.exit(1)

    print("LOADING STATUS: Loading programs...")
    print()

    print("Checking dependencies:")
    try:
        import pandas as pd
        print(f"[OK] pandas ({pd.__version__}) Data manipulation ready")

        import requests
        print(f"[OK] requests ({requests.__version__}) Network access ready")

        import matplotlib
        import matplotlib.pyplot as plt
        print(
            f"[OK] matplotlib ({matplotlib.__version__}) Visualization ready")

        import numpy as np
        run_analysis(pd, np, plt)

    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e.name}")
        print()
        print("To install the required packages, run:")
        # run in venv
        print("- Option 1 with pip:")
        print("pip install -r requirements.txt")
        # pip install poetry in global if command not found
        print("- Option 2 with Poetry:")
        print("poetry install")
        print("poetry run python3 loading.py")
        sys.exit(1)


def run_analysis(pd, np, plt) -> None:
    print()
    print("Analyzing Matrix data...")
    print("Processing 1000 data points...")

    # possible to use a seed for exact same graph
    np.random.seed(42)
    # numpy: create an array of numbers from 0 to 999
    x = np.arange(1000)
    # Create 1000 random decimal numbers
    y = np.random.rand(1000)

    # pandas: put them into a basic table (DataFrame)
    df = pd.DataFrame({
        "Time": x,
        "Value": y
    })

    print("Generating visualization...")
    print()
    # matplotlib: plot the table and save it
    plt.plot(df["Time"], df["Value"])
    plt.savefig("matrix_analysis.png")

    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    loading()
