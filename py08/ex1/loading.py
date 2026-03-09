# File: ex01/loading.py
import sys


def check_and_import() -> None:
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
        print(f"\n[ERROR] Missing dependency: {e.name}")
        print("To install the required packages, run:")
        print("Option 1 with pip: pip install -r requirements.txt")
        print("Option 2 with Poetry: poetry install")
        sys.exit(1)


def run_analysis(pd, np, plt) -> None:
    print("Analyzing Matrix data...")

    # 1. Use Numpy to generate 1000 simulated data points
    print("Processing 1000 data points...")
    # Generating a "Matrix Signal" (a sine wave with some random noise)
    x = np.linspace(0, 100, 1000)
    matrix_noise = np.random.normal(0, 0.5, 1000)
    y = np.sin(x) + matrix_noise

    # 2. Use Pandas to structure the data into a DataFrame
    df = pd.DataFrame({
        'Time': x,
        'Signal_Strength': y
    })

    # 3. Use Matplotlib to generate the visualization
    print("Generating visualization...")
    plt.figure(figsize=(10, 5))
    plt.plot(df['Time'], df['Signal_Strength'], color='green', linewidth=0.5)
    plt.title("Matrix Signal Anomalies")
    plt.xlabel("Time")
    plt.ylabel("Signal Strength")
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the file as required by the PDF
    filename = "matrix_analysis.png"
    plt.savefig(filename)

    print("Analysis complete!")
    print(f"Results saved to: {filename}")


if __name__ == "__main__":
    check_and_import()
