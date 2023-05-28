import os
from colorama import Fore
import add_extension_to_empty_files
import add_ext_to_ext
import delete_files
import rename_files
import remove_filext
import extensions_config

'''
enter the directory

#variables:
*directory - current directory
'''


def enter_directory() -> str:
    while True:
        directory: str = input(f"{Fore.LIGHTWHITE_EX}"
                               f"Enter path to directory:"
                               f"{Fore.RESET} ")
        try:
            if not os.path.exists(directory):
                raise ValueError(f"{Fore.RED}"
                                 f"The entered path does not exist."
                                 f"{Fore.RESET}")
            elif not os.path.isdir(directory):
                raise ValueError(f"{Fore.RED}"
                                 f"The entered path is not a directory."
                                 f"{Fore.RESET}")
        except ValueError as error:
            print(error)
        else:
            return directory


'''
Function to choose action

#variables:
*action - to select Rename or Delete
'''


def choose_action() -> int:
    while True:
        print(f"{Fore.LIGHTWHITE_EX}"
              f"Select an action to perform:"
              f"{Fore.RESET}")
        options = [
            "1. Rename files with a specific extension",
            "2. Delete files with a specific extension",
            "3. Remove files extension from the file",
            "4. Add extensions to empty files",
            "5. Add extension to files with specific extension",
        ]
        print("\n".join(options))
        length = len(options)
        try:
            action: int = int(input(f"{Fore.LIGHTWHITE_EX}"
                                    f"Enter selection (1-5):"
                                    f"{Fore.RESET} "))
            if 1 <= action <= length:
                return action
            else:
                print(f"{Fore.RED}"
                      f"Invalid input, please enter a number between 1 and {length}"
                      f"{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}"
                  f"Invalid input, please enter a number between 1 and {length}"
                  f"{Fore.RESET}")


'''
Function to perform action

#variables:
*directory - current directory to delete the file
*extension - picked file extension
*failed_file_path - file path to rename files
*deleted_file_path - file path for delete file
*action - entered action
'''


def perform_action(directory: str, extension: str, failed_file_path: str,
                   deleted_file_path: str, remove_filext_path: str, add_file_path: str,
                   add_ext_to_ext_file_path: str, action: int) -> None:
    lower_extension: str = extension.lower()
    if action == 1:
        rename_files.rename_files(directory, lower_extension, failed_file_path)
    elif action == 2:
        delete_files.delete_file_with_extension(directory, lower_extension, deleted_file_path)
    elif action == 3:
        remove_filext.remove_file_extension(directory, lower_extension, remove_filext_path)
    elif action == 4:
        add_extension_to_empty_files.add_extension(directory, lower_extension, add_file_path)
    elif action == 5:
        add_ext_to_ext.add_ext_to_ext(directory, lower_extension, add_ext_to_ext_file_path)


'''
Function to validate the input of the correct file extension. 
Accepts extensions '.!ut' || '.part'.

#variables:
*valid_extension - available extensions
*extension - file extension (.!ut || .part)
'''


def get_valid_extension() -> str:
    # Loop until a valid extension is entered
    while True:
        extension: str = input(f"{Fore.LIGHTWHITE_EX}"
                               f"Enter the file extension type (e.g. .!ut or .part):"
                               f"{Fore.RESET} ").strip().lower()
        if extension in extensions_config.valid_extension:
            return extension
        else:
            # print("Error: the extension must be either '.part' or '.!ut'")
            # print(f"Error: the extension must be either" + " or ".join(valid_extension))
            valid_extension_msg: str = " or ".join(extensions_config.valid_extension)
            error_msg: str = f"{Fore.RED}" \
                             f"Error: the extension must be either {valid_extension_msg}" \
                             f"{Fore.RESET}"
            print(error_msg.format(valid_extension_msg))


'''
Function for the 5th option.
Required to install the extension.
'''


def get_valid_extension_to_add_function() -> str:
    while True:
        try:
            extension: str = input(f"{Fore.LIGHTWHITE_EX}"
                                   f"Enter the extension to which you want to add "
                                   f"the previously selected (e.g. .txt): "
                                   f"{Fore.RESET} ").strip().lower()
            if not extension:
                raise ValueError(f"{Fore.RED}"
                                 f"Extension cannot be an empty string."
                                 f"{Fore.RESET}")
            if extension in extensions_config.duplication_extension:
                raise ValueError(f"{Fore.RED}"
                                 f"You cannot add an extension to .part or .!ut"
                                 f"{Fore.RESET}")
            if extension in extensions_config.valid_extensions:
                return extension
            else:
                valid_extension_msg: str = ", ".join(extensions_config.valid_extensions)
                error_msg: str = f"{Fore.RED}" \
                                 f"Error: the extension must be either {valid_extension_msg}" \
                                 f"{Fore.RESET}"
                print(error_msg.format(valid_extension_msg))
        except ValueError as ve:
            print(f"{Fore.RED}"
                  f"Error: {ve}"
                  f"{Fore.RESET}")


'''
Function calculates the file size in the appropriate units

#variables
*size - size in bytes, kb, mb, gb, tb
'''


def format_size(size: float) -> str:
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


'''elapsed_time - elapsed time of function'''


def format_elapsed_time(elapsed_time: float) -> str:
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    milliseconds = int(milliseconds * 1000)
    formatted_time = f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}.{milliseconds:03.0f}"
    return formatted_time
