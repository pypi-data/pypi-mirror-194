import os
import inspect

from .creator.avatar_creator import create_avatar
from .launcher.avatar_launcher import giftubing_main

def start():
    """
    Gets user input, whether to generate a new avatar 
    or use one.
    """
    choice_is_valid = False
    while not choice_is_valid:
        choice = input("\nPress 0 to create your avatar\nPress 1 to launch created avatar\n")
        try:
            choice = int(choice)
        except ValueError:
            print(f"Input must be an integer: {choice} is not valid")
        if choice < 0:
            print(f"{choice} must be greater than or equal to zero")
        elif choice > 1:
            print(f"{choice} must be below 2")
        else:
            choice_is_valid = True
    if choice == 0:
        create_avatar(os.path.dirname(inspect.stack()[1].filename))
    else:
        giftubing_main(os.path.dirname(inspect.stack()[1].filename))

if __name__ == "__main__":
    start()