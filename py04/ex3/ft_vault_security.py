def ft_vault_security() -> None:
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===")
    print()
    new_data = None
    print("Initiating secure vault access...")
    try:
        with open("classified_data.txt", "r") as vault:
            print("Vault connection established with failsafe protocols")
            print()
            print("SECURE EXTRACTION:")
            data: str = vault.read()
            print(data)
        with open("security_protocols.txt", "r") as protocol:
            new_data = protocol.read()
        print()
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
        return
    except Exception as e:
        print("ERROR:", e)
        return
    print("SECURE PRESERVATION:")
    try:
        if new_data:
            with open("classified_data.txt", "a") as vault:
                vault.write("\n" + new_data)
                print(new_data)
            print("Vault automatically sealed upon completion")
        else:
            print("ERROR: No data to preserve.")
        print()
        print("All vault operations completed with maximum security.")
    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    ft_vault_security()
