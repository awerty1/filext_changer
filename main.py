import os
import filext_changer
import create_files_test
# from termcolor import colored
from colorama import init

# We call this function to enable color support in the terminal.
# init()


if __name__ == '__main__':
    # directory = 'h:/CODE/Python/vogu project/File Extension/'
    # extension = '.!ut'
    # extension = '.part'
    # failed_file_path = input("Enter path to save failed file names: ")
    # failed_file_path = 'h:/CODE/Python/vogu project/File Extension/Failed rename files.txt'
    directory = input("Enter path to directory: ")
    create_files_test.create_files(directory)
    extension = filext_changer.get_valid_extension()
    failed_file_path = os.path.abspath(os.path.join(directory, 'Renamed files.txt'))
    deleted_file_path = os.path.abspath(os.path.join(directory, 'Deleted files.txt'))
    action = filext_changer.choose_action()
    filext_changer.perform_action(directory, extension, failed_file_path, deleted_file_path, action)
    # rename_files(directory, extension.lower(), failed_file_path)
