def get_resize_input(img_shape):
    """
    Gets user input for desired resizing of avatar to create.
    """
    print(f"\n\n\n\navatar image shape is {img_shape}, do you want to resize?")
    width_is_chosen = False
    height_is_chosen = False
    while not width_is_chosen:
        width = input("input width (enter to skip):")
        if width == "":
            print("width unchanged")
            width = img_shape[0]
            width_is_chosen = True
        try:
            width = int(width)
        except ValueError:
            print(f"Input must be an integer: {width} is not valid")
        if width < 0:
            print(f"{width} must be greater than or equal to zero")
        else:
            width_is_chosen = True
    while not height_is_chosen:
        height = input("input height (enter to keep ratio):")
        if height == "":
            height = (img_shape[1] * width) / img_shape[0]
            print("height to width ration kept")
            height_is_chosen = True
        try:
            height = int(height)
        except ValueError:
            print(f"Input must be an integer: {height} is not valid")
        if height < 0:
            print(f"{height} must be greater than or equal to zero")
        else:
            height_is_chosen = True
    newsize = (width, height)
    return newsize