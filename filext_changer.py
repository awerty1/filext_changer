import os
from datetime import datetime
# from termcolor import colored
from colorama import init, Fore, Style

# We call this function to enable color support in the terminal.
init()

'''
Function to choose action

#variables:
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
'''


def perform_action(directory, extension, failed_file_path, deleted_file_path, action):
    lower_extension = extension.lower()
    if action == 1:
        rename_files(directory, lower_extension, failed_file_path)
    elif action == 2:
        delete_file_with_extension(directory, lower_extension, deleted_file_path)


'''
Function to deleting extension
Deletes all files with the given extension in the given directory

#variables:
*directory - the directory to search for files
*extension - the file extension to delete (e.g., ".txt")
*return - a list of deleted filenames
'''


def delete_file_with_extension(directory, extension, deleted_file_path):
    file_counter = 0
    success_deleted_files = {}
    failed_deleted_files = {}
    try:
        print("")
        print(f"The extension change occurs in the directory {Fore.CYAN}{directory}{Fore.RESET}")
        for filename in os.listdir(directory):
            if filename.endswith(extension):
                filepath = os.path.join(directory, filename)
                file_size = os.path.getsize(filepath)
                try:
                    os.remove(filepath)
                    success_deleted_files[filename] = file_size
                    print(f"{file_counter + 1}. File "
                          f"{Fore.GREEN + Style.BRIGHT}{filename}{Style.RESET_ALL} "
                          f"was successfully deleted from {Fore.CYAN}{directory}{Fore.RESET}")
                except OSError:
                    failed_deleted_files[filename] = file_size
                    print(f"{file_counter + 1}. Failed to deleted file {Fore.LIGHTRED_EX}{filename}{Fore.RESET}")

                file_counter += 1

        deleted_files_count = len(success_deleted_files)
        msg1_for_1 = f"\nDeleting files completed successfully! {deleted_files_count} file were deleted."
        msg2_for_any = f"\nDeleting files completed successfully! {deleted_files_count} files were deleted."

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write status of deleted files to a file
        deleted_file_path = create_deleted_files_log(failed_deleted_files, success_deleted_files, deleted_file_path)

        failed_deleted_files_count = len(failed_deleted_files)
        msg1_for_1 = f"{failed_deleted_files_count} file failed to delete, check " \
                     f"{Fore.CYAN}{deleted_file_path}{Fore.RESET}"
        msg2_for_any = f"{failed_deleted_files_count} files failed to delete, check " \
                       f"{Fore.CYAN}{deleted_file_path}{Fore.RESET}"

        if failed_deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

    except FileNotFoundError:
        print(f"Directory {Fore.CYAN}{directory}{Fore.RESET} "
              f"does not exist")
    except Exception as e:
        print(f"An error occurred while deleting files: "
              f"{Fore.LIGHTRED_EX}{str(e)}{Fore.RESET}")


'''
Function for logging

#variables:
*failed_deleted_files -
*success_deleted_files -
*deleted_file_path -
'''


def create_deleted_files_log(failed_deleted_files, success_deleted_files, deleted_file_path):
    # create a new file (failed deleted files(count).txt) if such a file is already contained in the directory
    count = 1
    while os.path.exists(deleted_file_path):
        count += 1
        deleted_file_path = os.path.abspath(os.path.join(os.path.dirname(deleted_file_path),
                                                         f"Deleted files({count}).txt"))

    now = datetime.now()
    # format date as string e.g. "Sat 2023-05-13 17:12:36 PM"
    date_string = now.strftime("%a %Y-%m-%d %H:%M:%S %p %Z")
    # total size of deleted files
    total_size = sum(success_deleted_files.values())
    total_size = format_size(total_size)

    # write list of "unsuccessful deleted" of files
    with open(deleted_file_path, "w") as f:
        # write date followed by new line
        f.write("Current date: " + date_string + "\n")
        # write current directory
        f.write("Current directory: " + os.path.dirname(deleted_file_path) + "\n")
        # count of all deleted files
        f.write(f"Total deleted files: {len(success_deleted_files)}\n")
        # count of failed deleted files
        f.write(f"Total failed deleted files: {len(failed_deleted_files)}\n")
        # total size of deleted files
        f.write(f"Total size of deleted files: {total_size}\n\n")

        # write list of failed deleted files
        if failed_deleted_files:
            f.write('\n###########################')
            f.write(f"\n# Unsuccessful deleted {len(failed_deleted_files)}: #")
            f.write('\n###########################\n\n')
            # add a number to each line of the list of failed deleted
            for i, (file, file_size) in enumerate(failed_deleted_files.items(), start=1):
                file_label = format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all files deleted successfully
        elif success_deleted_files and not failed_deleted_files:
            f.write('\n##############################################')
            f.write('\n# Great job! All files deleted successfully! #')
            f.write('\n##############################################')
        # write msg if extension does not found in directory
        else:
            f.write('\n#######################################')
            f.write('\n# Files not found, no such extension! #')
            f.write('\n#######################################')

        # write list of successfully deleted files
        if success_deleted_files:
            f.write('\n\n#########################')
            f.write(f"\n# Successful deleted {len(success_deleted_files)}: #")
            f.write('\n#########################\n\n')
            # add a number to each line of the list of successful deleted
            for i, (file, file_size) in enumerate(success_deleted_files.items(), start=1):
                file_label = format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return deleted_file_path


'''
Function calculates the file size in the appropriate units

#variables
*size - bytes, kb, mb, gb, tb
'''


def format_size(size):
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


'''
Function to validate the input of the correct file extension. 
Accepts extensions '.!ut' || '.part'.

#variables:
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
A function that renames the extension ".! ut" to ".part" or vice versa.

#variables:
*directory - current directory
*extension - file extension
*failed_file_path - path to save failed files
*success_rename_files - list of successes renamed files
*failed_rename_files - list of failed renamed files
*counter - file counter
'''


def rename_files(directory, extension, failed_file_path):
    try:
        counter = 0
        failed_rename_files = {}
        success_rename_files = {}
        print("")
        print(f"The extension change occurs in the directory {Fore.CYAN}{directory}{Fore.RESET}")
        for filename in os.listdir(directory):
            if not filename.endswith(extension):
                continue

            old_filename = os.path.join(directory, filename)
            root, _ = os.path.splitext(old_filename)
            new_extension = '.part' if extension == '.!ut' else '.!ut'
            new_filename = root + new_extension
            new_filename_basename = os.path.basename(new_filename)
            file_size = os.path.getsize(old_filename)

            if os.path.exists(new_filename):
                print(f"{counter + 1} {Fore.LIGHTRED_EX}{new_filename}{Fore.RESET} "
                      f"- already exists, skipping")
                failed_rename_files[filename] = file_size
            else:
                os.rename(old_filename, new_filename)
                print(f"{counter + 1} {Fore.WHITE}{filename}{Fore.RESET} was renamed to "
                      f"{Fore.LIGHTGREEN_EX}{new_filename_basename}{Fore.RESET}")
                success_rename_files[filename] = file_size

            counter += 1

        success_rename_files_count = len(success_rename_files)
        msg1_for_1 = f"\nFile extension replacement completed successfully!" \
                     f" {success_rename_files_count} file were renamed."
        msg2_for_any = f"\nFile extension replacement completed successfully!" \
                       f" {success_rename_files_count} files were renamed."

        if success_rename_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write filed files to a file
        failed_file_path = create_rename_file_log(failed_rename_files, success_rename_files, failed_file_path)

        failed_rename_files_count = len(failed_rename_files)
        msg1_for_1 = f"{failed_rename_files_count} file failed to rename, check " \
                     f"{Fore.CYAN}{failed_file_path}{Fore.RESET}"
        msg2_for_any = f"{failed_rename_files_count} files failed to rename, check " \
                       f"{Fore.CYAN}{failed_file_path}{Fore.RESET}"

        if failed_rename_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

    except FileNotFoundError:
        print(f"Directory \"{directory}\" not found.")
    except OSError:
        print(f"Cannot access directory \"{directory}\".")


'''
A function to add information to a file about successes renamed files and files that cannot be renamed because they 
already exist.
The current date and message are also output to the file.

#variables:
*failed_rename_files - list of failed rename files
*success_rename_files - list of successes renamed files 
*failed_file_path - path to file (returned to refresh filename)
*date_string - current date
*count - counter for filename
'''


def create_rename_file_log(failed_rename_files, success_rename_files, failed_file_path):
    # create a new file (failed rename files(count).txt) if such a file is already contained in the directory
    count = 1
    while os.path.exists(failed_file_path):
        count += 1
        failed_file_path = os.path.abspath(os.path.join(os.path.dirname(failed_file_path),
                                                        f"Renamed files({count}).txt"))

    now = datetime.now()
    # format date as string e.g. "Sat 2023-05-13 17:12:36 PM"
    date_string = now.strftime("%a %Y-%m-%d %H:%M:%S %p %Z")
    # size of success renamed
    total_size = sum(success_rename_files.values())
    total_size = format_size(total_size)

    # write list of "unsuccessful rename" of files
    with open(failed_file_path, "w") as f:
        # write date followed by new line
        f.write("Current date: " + date_string + "\n")
        # write current directory
        f.write("Current directory: " + os.path.dirname(failed_file_path) + "\n")
        # count of all deleted files
        f.write(f"Total renamed files: {len(success_rename_files)}\n")
        # count of failed deleted files
        f.write(f"Total failed to renamed files: {len(failed_rename_files)}\n")
        # total size of deleted files
        f.write(f"Total size of renamed files: {total_size}\n\n")

        # write list of failed files
        if failed_rename_files:
            f.write('\n###########################')
            f.write(f"\n# Unsuccessful renames {len(failed_rename_files)}: #")
            f.write('\n###########################\n\n')
            # add a number to each line of the list of failed renames
            for i, (file, file_size) in enumerate(failed_rename_files.items(), start=1):
                file_label = format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all files rename successfully
        elif success_rename_files and not failed_rename_files:
            f.write('\n##############################################')
            f.write('\n# Great job! All files renamed successfully! #')
            f.write('\n##############################################')
        # write msg if extension does not found in directory
        else:
            f.write('\n#######################################')
            f.write('\n# Files not found, no such extension! #')
            f.write('\n#######################################')

        # write list of successfully renamed files
        if success_rename_files:
            f.write('\n\n#########################')
            f.write(f"\n# Successful renames {len(success_rename_files)}: #")
            f.write('\n#########################\n\n')
            # add a number to each line of the list of successful renames
            for i, (file, file_size) in enumerate(success_rename_files.items(), start=1):
                file_label = format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return failed_file_path


'''
if __name__ == '__main__':
    # directory = 'h:/CODE/Python/vogu project/File Extension/'
    # extension = '.!ut'
    # extension = '.part'
    # failed_file_path = input("Enter path to save failed file names: ")
    # failed_file_path = 'h:/CODE/Python/vogu project/File Extension/Failed rename files.txt'
    directory = input("Enter path to directory: ")
    extension = get_valid_extension()
    failed_file_path = os.path.abspath(os.path.join(directory, 'Renamed files.txt'))
    deleted_file_path = os.path.abspath(os.path.join(directory, 'Deleted files.txt'))
    action = choose_action()
    perform_action(directory, extension, failed_file_path, deleted_file_path, action)
    # rename_files(directory, extension.lower(), failed_file_path)
'''