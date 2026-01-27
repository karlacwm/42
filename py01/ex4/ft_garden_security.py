class SecurePlant:
    '''
    Protects plants data from invalid input values and direct access.
    '''

    def __init__(self, name: str, height: int, age: int) -> None:
        '''
        Sets the name, height in cm, and age in days of the plant.
        '''
        self._name: str = name
        self._height: int = height
        self._age: int = age

    def set_height(self, height: int) -> None:
        '''
        Sets the height of the plant if the value is valid.
        '''
        if height >= 0:
            self._height = height
            print(f"Height updated: {height}cm [OK]")
        else:
            print(
                f"\nInvalid operation attempted: height {height}cm"
                " [REJECTED]"
                "\nSecurity: Negative height rejected."
            )

    def set_age(self, age: int) -> None:
        '''
        Sets the age of the plant if the value is valid.
        '''
        if age >= 0:
            self._age = age
            print(f"Age updated: {age} days [OK]")
        else:
            print(
                f"\nInvalid operation attempted: age {age} days"
                + " [REJECTED]" + "\nSecurity: Negative age rejected."
            )

    def get_height(self) -> int:
        '''
        Returns the height of the plant.
        '''
        return self._height

    def get_age(self) -> int:
        '''
        Returns the age of the plant.
        '''
        return self._age


def ft_garden_security() -> None:
    '''
    Creates a secure plant and demonstrates the security features.
    No return value and no user input required.
    '''
    garden: list[SecurePlant] = [
        SecurePlant("Orchid", 40, 20),
        SecurePlant("Rose", 40, 20)
    ]
    print("=== Garden Security System ===")
    for plant in garden:
        print(f"Plant created: {plant._name}")
    SecurePlant.set_height(garden[0], 25)
    SecurePlant.set_age(garden[0], 5)
    SecurePlant.set_height(garden[0], -10)
    SecurePlant.set_age(garden[0], -5)
    print(
        f"\nCurrent plant: {garden[0]._name} "
        f"({plant.get_height()}cm, {plant.get_age()} days)"
    )


if __name__ == "__main__":
    ft_garden_security()
