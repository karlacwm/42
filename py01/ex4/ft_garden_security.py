'''
The Plant class is reused and the program creates a secure system that
prevent direct access and invalid data input, in this case the plant height.
'''


class SecurePlant:
    '''
    Protects plants data from invalid input values and direct access.
    '''

    def __init__(self, name: str, height: int, age: int) -> None:
        '''
        Sets the name, height in cm, and age in days of the plant.
        '''
        self._name: str = name
        self.__height: int = height
        self.__age: int = age

    def set_height(self, height: int) -> None:
        '''
        Sets the height of the plant if the value is valid.
        '''
        if height > 0:
            self.__height = height
            print(f"Height updated: {height}cm [OK]")
        else:
            print(
                f"\nInvalid operation attempted: height {height}cm"
                " [REJECTED]\nSecurity: Negative height rejected."
            )

    def set_age(self, age: int) -> None:
        '''
        Sets the age of the plant if the value is valid.
        '''
        if age > 0:
            self.__age = age
            print(f"Age updated: {age} days [OK]")
        else:
            print(
                f"\nInvalid operation attempted: age {age} days"
                " [REJECTED]\nSecurity: Negative age rejected."
            )

    def get_height(self) -> int:
        '''
        Returns the height of the plant.
        '''
        return self.__height

    def get_age(self) -> int:
        '''
        Returns the age of the plant.
        '''
        return self.__age


def ft_garden_security() -> None:
    '''
    Creates a secure plant and demonstrates the security features.
    No return value and no user input required.
    '''
    rose = SecurePlant("Rose", 40, 20)
    print("=== Garden Security System ===")
    print(f"Plant created: {rose._name}")
    SecurePlant.set_height(rose, rose.get_height())
    SecurePlant.set_age(rose, rose.get_age())
    SecurePlant.set_height(rose, -10)
    SecurePlant.set_age(rose, -5)
    print(
        f"\nCurrent plant: {rose._name} "
        f"({rose.get_height()}cm, {rose.get_age()} days)"
    )


if __name__ == "__main__":
    ft_garden_security()
