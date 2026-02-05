def get_id(name: str) -> str | None:
    try:
        return name + "_42"
    except Exception as e:
        print("Error:", e)
    # return
    finally:
        print("end")
    return name


print(get_id("ponyo"))
