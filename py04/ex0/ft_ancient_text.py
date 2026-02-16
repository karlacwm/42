def ft_ancient_text() -> None:
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===")
    print()
    file_name = "ancient_fragment.txt"
    file = None
    print("Accessing Storage Vault:", file_name)
    try:
        file = open(file_name, "r")
        print("Connection established...")
        print()
        data: str = file.read()
        print(data)
        print()
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
    except Exception as e:
        print("ERROR:", e)
    else:
        print("Data recovery complete. Storage unit disconnected.")
    finally:
        if file:
            file.close()


if __name__ == "__main__":
    ft_ancient_text()
