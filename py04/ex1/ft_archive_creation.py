def ft_archive_creation() -> None:
    print("===  CYBER ARCHIVES - PRESERVATION SYSTEM ===")
    file_name = "new_discovery.txt"
    print("Initializing new storage unit:", file_name)
    try:
        with open(file_name, "w") as file:
            print("Storage unit created successfully...")
            print()
            print("Inscribing presentation data...")
            if file_name == "new_discovery.txt":
                file.write("[ENTRY 001] New quantum algorithm discovered\n")
                file.write("[ENTRY 002] Efficiency increased by 347%\n")
                file.write("[ENTRY 003] Archived by Data Archivist trainee\n")
        with open(file_name, "r") as file:
            data = file.read()
            print(data)
    except Exception as e:
        print("Error caught:", e)
    else:
        print("Data inscription complete. Storage unit sealed.")
        print("Archive", file_name, "ready for long-term preservation.")


if __name__ == "__main__":
    ft_archive_creation()
