import os
from colorama import Fore

'''
Function to automatically create files in a directory
4testing

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


'''
Function to delete files without extension
4testing

#variables:
*directory - for choose directory
'''


def delete_files_without_extension(directory):
    try:
        # Get a list of files in a folder
        files = os.listdir(directory)
        # Go through all the files in a folder
        for file in files:
            # Check that it is a file without extension
            if not os.path.splitext(file)[1]:
                try:
                    # Delete a file
                    os.remove(os.path.join(directory, file))
                except OSError as e:
                    print(f"Error deleting {Fore.RED}{file}{Fore.RESET}: {e.strerror}")
    except OSError as e:
        # Display an error message in case of an error
        print(f"Error reading directory {directory}: {e.strerror}")

