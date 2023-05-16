import os
from datetime import datetime
# from termcolor import colored
from colorama import init, Fore, Style
import choose_action

# We call this function to enable color support in the terminal.
init()


'''
Function to deleting extension
Deletes all files with the given extension in the given directory

#variables:
*directory - the directory to search for files
*extension - the file extension to delete (e.g., ".txt")
*deleted_file_path - file path for delete file
*return - a list of deleted filenames
'''


def delete_file_with_extension(directory, extension, deleted_file_path):
    file_counter = 0
    success_deleted_files = {}
    failed_deleted_files = {}
    try:
        print("")
        print(f"The extension change occurs in the directory "
              f"{Fore.CYAN}{directory}{Fore.RESET}")

        for filename in os.listdir(directory):
            if filename.endswith(extension):
                filepath = os.path.join(directory, filename)
                file_size = os.path.getsize(filepath)
                try:
                    os.remove(filepath)
                    success_deleted_files[filename] = file_size
                    print(f"{file_counter + 1}. File "
                          f"{Fore.GREEN + Style.BRIGHT}{filename}{Style.RESET_ALL} "
                          f"was successfully deleted from "
                          f"{Fore.CYAN}{directory}{Fore.RESET}")
                except OSError:
                    failed_deleted_files[filename] = file_size
                    print(f"{file_counter + 1}. Failed to deleted file "
                          f"{Fore.LIGHTRED_EX}{filename}{Fore.RESET}")

                file_counter += 1

        deleted_files_count = len(success_deleted_files)
        msg1_for_1 = f"\nDeleting files completed successfully! " \
                     f"{deleted_files_count} file were deleted."
        msg2_for_any = f"\nDeleting files completed successfully! " \
                       f"{deleted_files_count} files were deleted."

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write status of deleted files to a file
        deleted_file_path = create_deleted_files_log(failed_deleted_files, success_deleted_files, deleted_file_path)

        failed_deleted_files_count = len(failed_deleted_files)
        msg1_for_1 = f"{failed_deleted_files_count} " \
                     f"file failed to delete, check " \
                     f"{Fore.CYAN}{deleted_file_path}{Fore.RESET}"
        msg2_for_any = f"{failed_deleted_files_count} " \
                       f"files failed to delete, check " \
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
*failed_deleted_files - file path for unsuccessfully renamed files
*success_deleted_files - dictionary of successfully deleted files
*deleted_file_path - file path for delete file
'''


def create_deleted_files_log(failed_deleted_files, success_deleted_files, deleted_file_path):
    # create a new file (failed deleted files(count).txt)
    # if such a file is already contained in the directory
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
    total_size = choose_action.format_size(total_size)

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
                file_label = choose_action.format_size(file_size)
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
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return deleted_file_path