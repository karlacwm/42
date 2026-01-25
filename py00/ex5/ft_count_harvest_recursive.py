def ft_count_harvest_recursive():
    harvest_day = int(input("Days until harvest: "))

    def recursive_counter(current_day):
        if current_day > harvest_day:
            print("Harvest time!")
            return
        else:
            print("Day", current_day)
        recursive_counter(current_day + 1)
    recursive_counter(1)
