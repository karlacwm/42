def ft_water_reminder():
    days_since_watered = int(input("Days since last watering: "))
    if days_since_watered > 2:
        print("Water the plants!")
    else:
        print("Plants are fine")
