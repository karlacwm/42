def ft_crisis_response() -> None:
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===")
    print()
    text_name = "lost_archive.txt"
    vault_name = "classified_vault.txt"
    file_name = "standard_archive.txt"
    try:
        print(f"CRISIS ALERT: Attempting access to '{text_name}'...")
        with open(text_name, "r") as text:
            data: str = text.read()
            print(data)
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
    except Exception as e:
        print("RESPONSE: Something went wrong -", e)
    finally:
        print("STATUS: Crisis handled, system stable")
    print()
    try:
        print(f"CRISIS ALERT: Attempting access to '{vault_name}'...")
        if "classified" in vault_name:
            raise PermissionError
        with open(vault_name, "w") as vault:
            vault.write("Trying to overwrite vault data")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
    except Exception as e:
        print("RESPONSE: Something went wrong -", e)
    finally:
        print("STATUS: Crisis handled, security maintained")
    print()
    try:
        print(f"ROUTINE ACCESS: Attempting access to '{file_name}'...")
        with open(file_name, "r") as file:
            data = file.read()
            print(f"SUCCESS: Archive recovered - \"{data}\"")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
    except Exception as e:
        print("RESPONSE: Something went wrong -", e)
    finally:
        print("STATUS: Normal operations resumed")
    print()
    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    ft_crisis_response()
