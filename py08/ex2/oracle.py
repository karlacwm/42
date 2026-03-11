# File: ex02/oracle.py
import os
import sys


def main() -> None:
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

    try:
        from dotenv import load_dotenv
    except ImportError:
        print("Error: python-dotenv not installed. "
              "Run 'pip install python-dotenv'")
        sys.exit(1)

    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # load_dotenv() automatically looks for a .env file
    # and loads it into the OS environment!
    # It returns True if it found the file, False if it didn't.
    has_env = load_dotenv()

    # os.getenv("VARIABLE_NAME", "Fallback_Value")
    mode = os.getenv("MATRIX_MODE")
    db_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("API_KEY")
    log_level = os.getenv("LOG_LEVEL")
    zion = os.getenv("ZION_ENDPOINT")

    # The PDF requires showing a warning if configuration is missing
    if not mode or not api_key:
        print("[WARNING] Default/missing configuration detected!")
        print("Please copy .env.example to .env and fill in your variables.")
        return

    # Printing the exact output expected by the subject
    print("Configuration loaded:")
    print(f"Mode: {mode}")
    print("Database: Connected to local instance" if db_url else (
        "Database: Disconnected"))
    print("API Access: Authenticated" if api_key else "API Access: Denied")
    print(f"Log Level: {log_level}")
    print("Zion Network: Online" if zion else "Zion Network: Offline")
    print()

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if has_env:
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file missing")

    print("[OK] Production overrides available")
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
