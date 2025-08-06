from colorama import Fore, Style, Back, init

from .reports_pkg import red_color, green_color, normal_color

def error_msg() -> str :
    """
    Returns the terminal formatted error message.

    Returns:
        str: Terminal string for an error message.
    """
    
    return f"{red_color} ERROR : {normal_color}"


def valid_msg() -> str :
    """
    Returns the terminal formatted validation message.

    Returns:
        str: Terminal string for a validation message.
    """
    
    # return f"{green_color} SUCCESSFUL : {normal_color}"
    return Fore.WHITE + Back.GREEN + "SUCCESSFUL :" + Style.RESET_ALL