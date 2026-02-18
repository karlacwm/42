def ft_archive_creation() -> None:
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===")
    print()
    file_name = "new_discovery.txt"
    file = None
    try:
        print("Initializing new storage unit:", file_name)
        open(file_name, "x")
        file = open(file_name, "w")
        print("Storage unit created successfully...")
        print()
        print("Inscribing preservation data...")
        entries: list[str] = [
            "[ENTRY 001] New quantum algorithm discovered",
            "[ENTRY 002] Efficiency increased by 347%",
            "[ENTRY 003] Archived by Data Archivist trainee"
        ]
        for entry in entries:
            file.write(f"{entry}\n")
            print(entry)
        print()
    except FileExistsError as e:
        print("ERROR:", e)
        print("Operation stopped to avoid overwriting an existing archive.")
    except Exception as e:
        print("ERROR:", e)
    else:
        print("Data inscription complete. Storage unit sealed.")
        print(f"Archive '{file_name}' ready for long-term preservation.")
    finally:
        if file:
            file.close()


if __name__ == "__main__":
    ft_archive_creation()
