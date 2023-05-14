import os
from datetime import datetime
# from termcolor import colored
from colorama import init, Fore, Style

# вызываем эту функцию, чтобы включить поддержку цветов в терминале
init()

'''
Function to choose action

#variables:
'''


def choose_action():
    while True:
        print("Select an action to perform:")
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
    deleted_files = []
    failed_deleted_files = []
    try:
        print("")
        print(f"The extension change occurs in the directory {Fore.CYAN}{directory}{Fore.RESET}")
        for filename in os.listdir(directory):
            if filename.endswith(extension):
                filepath = os.path.join(directory, filename)
                try:
                    os.remove(filepath)
                    deleted_files.append(filename)
                    print(f"{file_counter + 1}. File "
                          f"{Fore.GREEN + Style.BRIGHT}{filename}{Style.RESET_ALL} "
                          f"was successfully deleted from {Fore.CYAN}{directory}{Fore.RESET}")
                except:
                    failed_deleted_files.append(filename)
                    print(f"{file_counter + 1}. Failed to deleted file {Fore.LIGHTRED_EX}{filename}{Fore.RESET}")

                file_counter += 1

        deleted_files_count = len(deleted_files)
        msg1_for_1 = f"\nDeleting files completed successfully! {deleted_files_count} file were deleted."
        msg2_for_any = f"\nDeleting files completed successfully! {deleted_files_count} files were deleted."

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write filed files to a file
        # failed_file_path = rename_with_status_messages(failed_rename_files, success_rename_files, failed_file_path)

        failed_deleted_files_count = len(failed_deleted_files)
        msg1_for_1 = f"{failed_deleted_files_count} file failed to delete, check {Fore.CYAN}" \
                     f"{deleted_file_path}{Fore.RESET}"
        msg2_for_any = f"{failed_deleted_files_count} files failed to delete, check {Fore.CYAN}" \
                       f"{deleted_file_path}{Fore.RESET}"

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
        return deleted_files, failed_deleted_files


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
        failed_rename_files = []
        success_rename_files = []
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

            if os.path.exists(new_filename):
                print(f"{counter + 1} {Fore.LIGHTRED_EX}{new_filename}{Fore.RESET} "
                      f"- already exists, skipping")
                failed_rename_files.append(filename)
            else:
                os.rename(old_filename, new_filename)
                print(f"{counter + 1} {Fore.WHITE}{filename}{Fore.RESET} was renamed to "
                      f"{Fore.LIGHTGREEN_EX}{new_filename_basename}{Fore.RESET}")
                success_rename_files.append(filename)

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
        failed_file_path = rename_with_status_messages(failed_rename_files, success_rename_files, failed_file_path)

        failed_rename_files_count = len(failed_rename_files)
        msg1_for_1 = f"{failed_rename_files_count} file failed to rename, check {Fore.CYAN}" \
                     f"{failed_file_path}{Fore.RESET}"
        msg2_for_any = f"{failed_rename_files_count} files failed to rename, check {Fore.CYAN}" \
                       f"{failed_file_path}{Fore.RESET}"

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


def rename_with_status_messages(failed_rename_files, success_rename_files, failed_file_path):
    # create a new file (failed rename files(count).txt) if such a file is already contained in the directory
    count = 1
    while os.path.exists(failed_file_path):
        count += 1
        failed_file_path = os.path.abspath(os.path.join(directory, f"Renamed files({count}).txt"))

    now = datetime.now()
    # format date as string e.g. "Sat 2023-05-13 17:12:36 PM"
    date_string = now.strftime("%a %Y-%m-%d %H:%M:%S %p %Z")

    # write list of "unsuccessful rename" of files
    with open(failed_file_path, "w") as f:
        # write date followed by new line
        f.write("Current date " + date_string + "\n\n")

        # write list of failed files
        if failed_rename_files:
            f.write('\n###########################')
            f.write(f"\n# Unsuccessful renames {len(failed_rename_files)}: #")
            f.write('\n###########################\n\n')
            # add a number to each line of the list of failed renames
            for i, file in enumerate(failed_rename_files, start=1):
                f.write(f"{i}. {file}\n")
        # write msg is all files rename successfully
        elif success_rename_files and not failed_rename_files:
            f.write('\n##############################################')
            f.write('\n# Great job! All files renamed successfully! #')
            f.write('\n##############################################')
        # write msg if directory is empty
        else:
            f.write('\n############################################')
            f.write('\n# Directory is empty, no files were found! #')
            f.write('\n############################################')

        # write list of successfully renamed files
        if success_rename_files:
            f.write('\n\n#########################')
            f.write(f"\n# Successful renames {len(success_rename_files)}: #")
            f.write('\n#########################\n\n')
            # add a number to each line of the list of successful renames
            for i, file in enumerate(success_rename_files, start=1):
                f.write(f"{i}. {file}\n")
    return failed_file_path


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
