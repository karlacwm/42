def ft_count_harvest_iterative():
    days = int(input("Days until harvest: "))
    for count in range(1, days + 1):
        print("Day", count)
    print("Harvest time!")
