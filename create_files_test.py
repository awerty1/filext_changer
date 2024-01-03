import os

from colorama import Fore

'''
Function to automatically create files in a directory
4testing

#variables:
*directory - for choose directory
*extension - for extension of the file
'''


def create_files(directory: str, extension: str) -> None:
    try:
        # create directory if it does not exist
        # os.makedirs(directory, exist_ok=True)
        # filename_ext = ''
        # create 5 files in the folder
        for file_counter in range(1, 6):
            filename_ext = os.path.join(directory, f"test_file{file_counter}{extension}")
            filename_ext_basename = os.path.basename(filename_ext)
            try:
                # create an empty file with '.part' or '.!ut' extension
                open(filename_ext, 'w').close()
            except PermissionError:
                print(f"{Fore.RED}Failed to create file{Fore.RESET} "
                      f"{Fore.BLUE}{filename_ext_basename}{Fore.RESET} "
                      f"{Fore.RED}in the directory{Fore.RESET} "
                      f"{Fore.BLUE}{directory}{Fore.RESET}")
    except OSError:
        print(f"{Fore.RED}Failed to create directory{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET}.")


'''
Function to delete files without extension
4testing

#variables:
*directory - for choose directory
'''


def delete_files_without_extension(directory: str) -> None:
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
                    print(f"{Fore.RED}Error deleting{Fore.RESET} "
                          f"{Fore.BLUE}{file}{Fore.RESET}: "
                          f"{Fore.RED}{e.strerror}{Fore.RESET}")
    except OSError as e:
        # Display an error message in case of an error
        print(f"{Fore.RED}Error reading directory "
              f"{Fore.BLUE}{directory}{Fore.RESET}: {e.strerror}{Fore.RESET}")
