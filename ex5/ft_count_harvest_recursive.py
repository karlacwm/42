def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def recursive_counter(days):
        if days > 0:
            print("Day", days)
            recursive_counter(days - 1)
        else:
            print("Harvest time!")
    recursive_counter(days)
