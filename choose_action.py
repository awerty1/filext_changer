import os
from colorama import Fore
import delete_files
import rename_files

'''
enter the directory

#variables:
*directory - current directory
'''


def enter_directory():
    while True:
        directory = input("Enter path to directory: ")
        try:
            if not os.path.exists(directory):
                raise ValueError("The entered path does not exist.")
            elif not os.path.isdir(directory):
                raise ValueError("The entered path is not a directory.")
        except ValueError as error:
            print(error)
        else:
            return directory


'''
Function to choose action

#variables:
*action - to select Rename or Delete
'''


def choose_action():
    while True:
        print(f"{Fore.LIGHTYELLOW_EX}Select an action to perform:{Fore.RESET}")
        print("1. Rename files with a specific extension")
        print("2. Delete files with a specific extension")

        action = int(input("Enter selection (1 or 2): "))
        if action == 1 or action == 2:
            return action
        else:
            print("Invalid input, please enter 1 or 2")


'''
Function to perform action

#variables:
*directory - current directory to delete the file
*extension - picked file extension
*failed_file_path - file path to rename files
*deleted_file_path - file path for delete file
*action - entered action
'''


def perform_action(directory, extension, failed_file_path, deleted_file_path, action):
    lower_extension = extension.lower()
    if action == 1:
        rename_files.rename_files(directory, lower_extension, failed_file_path)
    elif action == 2:
        delete_files.delete_file_with_extension(directory, lower_extension, deleted_file_path)


'''
Function to validate the input of the correct file extension. 
Accepts extensions '.!ut' || '.part'.

#variables:
*valid_extension - available extensions
*extension - file extension (.!ut || .part)
'''


def get_valid_extension():
    # Loop until a valid extension is entered
    valid_extension = ('.!ut', '.part')
    while True:
        extension = input("Enter the file extension type (e.g. .!ut or .part): ")
        if extension.lower() in valid_extension:
            return extension
        else:
            print("Error: the extension must be either '.part' or '.!ut'")


'''
Function calculates the file size in the appropriate units

#variables
*size - size in bytes, kb, mb, gb, tb
'''


def format_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"
