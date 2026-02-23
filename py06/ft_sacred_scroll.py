import alchemy

def direct_module_access() -> None:
    print("Testing direct module access:")
    fire = alchemy.elements.create_fire()
    print("alchemy.elements.create_fire():", fire)
    water = alchemy.elements.create_water()
    print("alchemy.elements.create_water():", water)
    earth = alchemy.elements.create_earth()
    print("alchemy.elements.create_earth():", earth)
    air = alchemy.elements.create_air()
    print("alchemy.elements.create_air():", air)
    print()


def package_level_access() -> None:
    print("Testing package-level access (controlled by __init__.py):")
    fire = alchemy.create_fire()
    print("alchemy.create_fire():", fire)
    water = alchemy.create_water()
    print("alchemy.create_water():", water)
    try:
        earth = alchemy.create_earth()
        print("alchemy.create_earth():", earth)
    except AttributeError:
        print("alchemy.create_earth():", end=" ")
        print("AttributeError - not exposed")
    try:
        air = alchemy.create_air()
        print("alchemy.create_air():", air)
    except AttributeError:
        print("alchemy.create_air():", end=" ")
        print("AttributeError - not exposed")    
    print()

def ft_sacred_scroll() -> None:
    print("=== Sacred Scroll Mastery ===")
    print()
    direct_module_access()
    package_level_access()
    print("Package metadata:")
    print("Version:", alchemy.__version__)
    print("Author:", alchemy.__author__)


if __name__ == "__main__":
    ft_sacred_scroll()