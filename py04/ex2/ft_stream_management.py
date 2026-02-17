import sys


def ft_stream_management() -> None:
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===")
    print()
    try:
        print("Input Stream active. Enter archivist ID: ", end=" ")
        archivist_id: str = input()
        print("Input Stream active. Enter status report: ", end=" ")
        status_report: str = input()
        print()
        print(
            f"[STANDARD] Archive status from {archivist_id}: {status_report}")
        print("[ALERT] System diagnostic: Communication channels verified",
              file=sys.stderr)
        print("[STANDARD] Data transmission complete")
        print()
    except Exception as e:
        print("Error:", e, file=sys.stderr)
    else:
        print("Three-channel communication test successful.")


if __name__ == "__main__":
    ft_stream_management()
