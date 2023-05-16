import os
from colorama import Fore


def create_files(directory):
    try:
        # create directory if it does not exist
        #os.makedirs(directory, exist_ok=True)
        filename_ut = ''
        filename_part = ''
        for file in range(1, 6):
            try:
                filename_ut = os.path.join(directory, f"file{file}.!ut")
                filename_part = os.path.join(directory, f"file{file}.part")
                # create an empty file with .txt extension
                open(filename_ut, 'w').close()
                # create an empty file with .part extension
                open(filename_part, 'w').close()
            except PermissionError:
                print(f"Failed to create file "
                      f"{Fore.RED}{os.path.basename(filename_ut)}{Fore.RESET} "
                      f"or {Fore.RED}{os.path.basename(filename_part)}{Fore.RESET}"
                      f" in the directory "
                      f"{Fore.CYAN}{directory}{Fore.RESET}")
    except OSError:
        print(f"Failed to create directory "
              f"{Fore.CYAN}{directory}{Fore.RESET}.")
