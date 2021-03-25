import json
import os
from Utilities import utility_methods
from Utilities import subprocess_helper as sp
import re

json_file = "../WebBeast/Wordlists/word_lists.json"  # File containing wordlists
all_extensions = "../WebBeast/Wordlists/all_extensions.txt"  # File containing all extensions

'''
    Method: word_lists
    Purpose: To extract wordlists (specified by user) for a given service.
'''


def word_lists(service_selection, wordlist_selection):
    service_list = json_file_exists(json_file)  # Load word_lists from json file in a format python recognizes
    # Iterate over first dictionary grabbing service as key
    # Example: {"dirb": [{"big": "/usr/share/wordlists/dirb/big.txt"}]} - service key = "dirb"
    for service in service_list[service_selection]:
        # Iterate over list of dictionaries i.e. for dictionary in list
        # [{"big": "/usr/share/wordlists/dirb/big.txt"}, {"small": "/usr/share/wordlists/dirb/small.txt"}]
        # Grab key value pair from list of dictionaries
        # Example: key = 'big' and value = '/usr/share/wordlists/dirb/big.txt'
        for key, value in service.items():
            # {"big": "/usr/share/wordlists/dirb/big.txt"}
            if key == wordlist_selection:  # key = "big"
                return str(value)  # value = /usr/share/wordlists/dirb/big.txt

    return None  # If the wordlist does note exist return none


'''
    Method: display_word_list
    Purpose: To display wordlists available for each service i.e. apache:common
'''


def display_word_list():
    dictionary = json_file_exists(json_file)  # Load word_lists from json file in a format python recognizes
    # Iterate over every service key i.e. dirb,wordpress,apache and grab their corresponding list of dictionaries
    # Example:  [{'big': '/usr/share/wordlists/dirb/big.txt'}, {'small': '/usr/share/wordlists/dirb/small.txt'}]
    for service_key, list_of_dictionaries in dictionary.items():
        count = 1
        # Iterate over every dictionary corresponding to a particular service
        # Example: [{"big": "/usr/share/wordlists/dirb/big.txt"}]
        for dictionary in list_of_dictionaries:
            # Grab each dictionaries wordlist
            # Example: {"big": "/usr/share/wordlists/dirb/big.txt"} - key = "big"
            for wordlist_key in dictionary:
                if count == 1:
                    print("" + service_key)
                    print("  > " + service_key + ":" + wordlist_key)  # dirb:big
                    count = count + 1
                else:
                    print("  > " + service_key + ":" + wordlist_key)


'''
    Function: json_config_file_exists
    Purpose: Return true if json file exists (false otherwise).
'''


def json_file_exists(json_file):
    with open_file(json_file, "r") as file:  # Open json file for reading
        return json.load(file)  # load json python in python format and return results


'''
    Method: prepare_scan_results_file
    Purpose: Create file with ip and port descriptors for tool output.
'''


def prepare_scan_results_file(ip, port):
    file_path = utility_methods.get_current_directory()  # Save current directory as file path
    file_name = f"{ip}_port_{port}_scan_results"  # Create file name with ip and port
    complete_path = os.path.join(file_path, file_name + ".txt")  # Join file path and file name
    return complete_path  # Return the complete file path


'''
    Method: remove_emtpy_lines
    Purpose: Remove any empty lines that may occur from tool output.
'''


def remove_empty_lines(file_name):
    if not os.path.isfile(file_name):  # Check if file exists
        print(f"{file_name} does not exist")  # Let user know file does not exist
        return  # Exit method
    with open(file_name, 'rw') as file_handle:  # Open file for reading and writing
        lines = file_handle.readlines()  # Read file line by line
        lines = filter(lambda empty_line: empty_line.strip(), lines)  # Strip all empty lines in file
        file_handle.writelines(lines)  # Write stripped lines back to file

    file_handle.close()


'''
    Method: display_file_extensions
    Purpose: List all available file extensions.
'''


def display_file_extensions():
    with open_file(all_extensions, 'r') as file:
        for line in file:
            print(line, end='')

        print()
    file.close()


'''
    Method: exit_handler
    Purpose: Remove all HTTP error codes 204,302,307,401,403 and output results to file.filtered
'''


def filter_codes(file_path):
    file_path = remove_file_extension(file_path)
    # Remove any line in file with coinating codes 204,302,307,401,403
    command = f"sed '/204\|302\|307\|401\|403/d' {file_path}.temp > {file_path}.filtered"
    return sp.run(command)  # Run commands in shell


'''
    Method: remove_file_extension
    Purpose: Purpose: Remove file extension .txt
'''


def remove_file_extension(file):
    return file.replace(".txt", '')  # Remove .txt extension


'''
    Method: clean_file
    Purpose: Extract all useful info from dirsearch output. 
             Example: [14:21:43] 403 -    1KB - /webalizer
'''


def clean_file(file):
    pattern = re.compile(r'(\[\d\d:\d\d:\d\d\]\s\d\d\d)+')  # Pattern finds [14:21:43] 403
    pattern_remove = re.compile(r'(\[\d\d:\d\d:\d\d\])')  # Pattern find [14:21:43]
    with open_file(file, 'r') as read_file:
        for line in read_file:
            with open_file(f"{remove_file_extension(file)}.temp", 'a') as write_file:
                match = re.search(pattern, line)  # Search for [14:21:43] 403
                if (match):
                    new_line = re.sub(pattern_remove, '', line)  # Replace [14:21:43] with space
                    write_file.write(new_line)  # Write filtered line to file

    read_file.close()
    write_file.close()


'''
   Method: list_to_string
   Purpose: Convert list to string using list comprehension 
'''


def list_to_string(lst):
    return ' '.join(map(str, lst))


'''
    Method: create_custom_wordlist
    Purpose: Remove all duplicate directory entries between lists
'''


def create_custom_wordlist(wl, ip):
    combine_lists = f"cat {wl} | awk '!visited[$0]++' > {ip}_custom_wordlist.txt"
    return sp.run(combine_lists)


def split_list(word_list, lst):
    # Split key value pairs separated by colon example dirb:big splits key "dirb" and value "big"
    split_lst = word_list[lst].split(":")
    wordlist_name = split_lst[0]  # Grab key example "dirb"
    wordlist_selection = split_lst[1]  # Grab value example "big"
    return wordlist_name, wordlist_selection


def combine_lists(word_list):
    wordlists_to_combine = []
    # Word_list example: ['dirb:small', 'dirsearch:default']
    list_length = len(word_list)  # Get number of wordlists
    for lst in range(list_length):  # Iterate over each list in list range
        # Split key value pairs separated by colon example dirb:big splits key "dirb" and value "big"
        wordlist_name, wordlist_selection = split_list(word_list, lst)
        wordlists_to_combine.append(word_lists(wordlist_name, wordlist_selection))

    return wordlists_to_combine  # Example ["/usr/share/wordlists/dirb/big.txt","/usr/share/wordlists/dirb/small.txt"]


def open_file(temp_file, mode):
    file = ''
    try:
        file = open(temp_file, mode)
    except IOError:
        print(f"An error was found. Either path {temp_file} is incorrect or file doesn't exist!")

    return file
