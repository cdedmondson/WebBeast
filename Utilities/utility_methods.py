import os
import socket
from colorama import Fore, Style

'''
    Method: get_current_directory
    Purpose: Return current working directory.
'''


def get_current_directory():
    return os.getcwd()  # Return current working directory


'''
    Method: is_valid_ip
    Purpose: Check if ip is valid.
'''


def is_valid_ip(ip):
    try:
        if socket.gethostbyname(ip) == ip:
            return True
        else:
            return False
    except socket.gaierror:
        print(colors('bred', f'[!] Invalid format {ip}'))


'''
    Method: is_valid_port
    Purpose: Make port is within a valid range.
'''


def is_valid_port(port):
    if 1 <= port <= 65535:
        return True
    else:
        return False


'''
    Method: port_443
    Purpose: Check if port is HTTPS
'''


def port_443(port):
    if port == 443:
        return True
    else:
        return False


'''
    Method: check_range
    Purpose: Check if thread count is within valid range
'''


def check_range(threads):
    if 1 <= threads <= 50:
        return True
    else:
        return False


'''
    Method: getlist_values
    Purpose: Turn double list to single i.e. from [['dirb:common','dirb:large']] to ['dirb:commmon','dirb:large']
'''


def getlist_values(scan_list):
    temp_list = []
    for lst in scan_list:
        for index in lst:
            temp_list.append(index)

    return temp_list


def colors(color, string):
    color_values = {
        'bgreen': Fore.GREEN + Style.BRIGHT,
        'bred': Fore.RED + Style.BRIGHT,
        'bblue': Fore.BLUE + Style.BRIGHT,
        'byellow': Fore.YELLOW + Style.BRIGHT,
        'bmagenta': Fore.MAGENTA + Style.BRIGHT,

        'green': Fore.GREEN,
        'red': Fore.RED,
        'blue': Fore.BLUE,
        'yellow': Fore.YELLOW,
        'magenta': Fore.MAGENTA,

        'rst': Fore.RESET,
    }

    return color_values[color] + string + color_values['rst']
