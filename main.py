import os
import create_files_test
import choose_action
# from termcolor import colored
from colorama import init, Fore

# We call this function to enable color support in the terminal.
# init()

'''
main_conf - configure from variables
Can be used to remove multiple permissions in 1 folder or in different folders.
This can be done in the "perform_action" function.
'''


def main_conf():
    # directory of the folder
    directory = 'h:/CODE/Python/vogu project/File Extension/fd/'

    # extension of file
    extension_ut = '.!ut'
    extension_part = '.part'

    # 1 - rename , 2 - delete , 3 - remove
    action = 2

    # function to auto-create files
    create_files_test.create_files(directory, extension_ut)
    create_files_test.create_files(directory, extension_part)

    # function to auto-delete files
    create_files_test.delete_files_without_extension(directory)

    # selected directory to will create file and name
    name_of_renamed_files = 'Renamed files.txt'
    name_of_deleted_files = 'Deleted files.txt'
    name_of_remove_extensions_file = 'Removed extension.txt'
    failed_file_path = os.path.abspath(os.path.join(directory, name_of_renamed_files))
    deleted_file_path = os.path.abspath(os.path.join(directory, name_of_deleted_files))
    remove_filext_path = os.path.abspath(os.path.join(directory, name_of_remove_extensions_file))

    # function to perform action
    choose_action.perform_action(directory, extension_ut, failed_file_path,
                                 deleted_file_path, remove_filext_path, action)
    choose_action.perform_action(directory, extension_part, failed_file_path,
                                 deleted_file_path, remove_filext_path, action)


'''
main function
filling from console
'''


def main():
    name_of_renamed_files = 'Renamed files.txt'
    name_of_deleted_files = 'Deleted files.txt'
    name_of_remove_extensions_file = 'Removed extension.txt'
    name_of_added_ext_file = 'Added extension.txt'
    name_of_added_ext_to_ext_file = 'Added extension to extension.txt'
    while True:
        directory = choose_action.enter_directory()
        extension = choose_action.get_valid_extension()
        #create_files_test.create_files(directory, extension)
        #create_files_test.delete_files_without_extension(directory)
        failed_file_path = os.path.abspath(os.path.join(directory, name_of_renamed_files))
        deleted_file_path = os.path.abspath(os.path.join(directory, name_of_deleted_files))
        remove_filext_path = os.path.abspath(os.path.join(directory, name_of_remove_extensions_file))
        add_file_path = os.path.abspath(os.path.join(directory, name_of_added_ext_file))
        name_of_added_ext_to_ext_file = os.path.abspath(os.path.join(directory, name_of_added_ext_to_ext_file))
        action = choose_action.choose_action()
        choose_action.perform_action(directory, extension, failed_file_path,
                                     deleted_file_path, remove_filext_path, add_file_path,
                                     name_of_added_ext_to_ext_file, action)
        user_input = input(f"\n{Fore.LIGHTWHITE_EX}"
                           f"Do you want to continue? (y/n):"
                           f"{Fore.RESET} ")
        if user_input.lower() == "y":
            continue
        else:
            break


if __name__ == '__main__':
    main()
    # main_conf()
