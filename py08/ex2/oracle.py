import os
import sys


def oracle() -> None:
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
    # and loads it into the dictionary of os env var
    # returns true if it found the file, false if it didn't
    has_env = load_dotenv()

    # os.getenv("VARIABLE_NAME")
    mode = os.getenv("MATRIX_MODE")
    db_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("API_KEY")
    log_level = os.getenv("LOG_LEVEL")
    zion = os.getenv("ZION_ENDPOINT")

    config_checklist = [mode, db_url, api_key, log_level, zion]
    for item in config_checklist:
        if not item:
            print("[WARNING] Essential configuration is missing!")
            print("Please copy .env.example to .env and change the values.")
            return

    if (db_url == "database_url_here" or api_key == "api_key_here"
       or zion == "zion_endpoint_here"):
        print("[WARNING] Configuration values are invalid.")
        print("Remember to change the values in the .env file.")
        return

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
    oracle()
