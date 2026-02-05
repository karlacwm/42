def get_id(name: str):
    try:
        return name + "_42"
    except Exception as e:
        print("Error:", e)
    return
    finally:
        print("end")


print(get_id(2))
