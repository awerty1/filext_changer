import os
from colorama import Fore

'''
Function to automatically create files in a directory

#variables:
*directory - for choose directory
*extension - for extension of the file
'''


def create_files(directory, extension):
    try:
        # create directory if it does not exist
        # os.makedirs(directory, exist_ok=True)
        filename_ext = ''
        # create 5 files in the folder
        for file in range(1, 6):
            try:
                filename_ext = os.path.join(directory, f"test_file{file}{extension}")
                # create an empty file with .part or .!ut extension
                open(filename_ext, 'w').close()
            except PermissionError:
                print(f"Failed to create file "
                      f"{Fore.RED}{os.path.basename(filename_ext)}{Fore.RESET}"
                      f" in the directory "
                      f"{Fore.CYAN}{directory}{Fore.RESET}")
    except OSError:
        print(f"Failed to create directory "
              f"{Fore.CYAN}{directory}{Fore.RESET}.")
