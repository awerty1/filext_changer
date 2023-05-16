import os
import create_files_test
import choose_action
# from termcolor import colored
# from colorama import init

# We call this function to enable color support in the terminal.
# init()

'''
main_conf - configure from variables
Can be used to remove multiple permissions in 1 folder or in different folders.
This can be done in the "perform_action" function.
'''


def main_conf():
    directory = 'h:/CODE/Python/vogu project/File Extension/fd/'
    extension_ut = '.!ut'
    extension_part = '.part'
    action = 2
    failed_file_path = os.path.abspath(os.path.join(directory, 'Renamed files.txt'))
    deleted_file_path = os.path.abspath(os.path.join(directory, 'Deleted files.txt'))
    create_files_test.create_files(directory)
    choose_action.perform_action(directory, extension_ut, failed_file_path, deleted_file_path, action)
    choose_action.perform_action(directory, extension_part, failed_file_path, deleted_file_path, action)


'''
main function
filling from console
'''


def main():
    directory = input("Enter path to directory: ")
    create_files_test.create_files(directory)
    extension = choose_action.get_valid_extension()
    failed_file_path = os.path.abspath(os.path.join(directory, 'Renamed files.txt'))
    deleted_file_path = os.path.abspath(os.path.join(directory, 'Deleted files.txt'))
    action = choose_action.choose_action()
    choose_action.perform_action(directory, extension, failed_file_path, deleted_file_path, action)


if __name__ == '__main__':
    main()
    main_conf()
