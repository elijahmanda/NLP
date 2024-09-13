from colorama import Fore


def print_color(color, *args, **kwargs):
    print(color, *args, Fore.RESET, **kwargs)
