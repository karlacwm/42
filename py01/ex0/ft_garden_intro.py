def ft_garden_intro() -> None:
    '''
    Displays information about a plant in my garden,
    including its name, height, and age.
    '''
    plant: str = "Orchid"
    height: int = 40
    age: int = 20
    plant_information: str = (
        f"Plant: {plant}\n"
        f"Height: {height}cm\n"
        f"Age: {age} days\n"
    )
    print("=== Welcome to My Garden ===")
    print(plant_information)
    print("=== End of Program ===")


if __name__ == "__main__":
    ft_garden_intro()
