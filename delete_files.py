import os
import time
from datetime import datetime

from colorama import init, Fore, Style

import choose_action
import constants as cnst

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
    start_time = time.time()
    file_counter = 1
    success_deleted_files = {}
    failed_deleted_files = {}
    try:
        print(f"\n{Fore.LIGHTWHITE_EX}"
              f"Deletion of files with the selected extension occurs in the directory:"
              f"{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET}")

        for filename in os.listdir(directory):
            if filename.lower().endswith(extension):
                filepath = os.path.join(directory, filename)
                file_size = os.path.getsize(filepath)
                try:
                    os.remove(filepath)
                    success_deleted_files[filename] = file_size
                    print(f"{file_counter}. "
                          f"{Fore.GREEN}File{Fore.RESET} "
                          f"{Fore.BLUE + Style.BRIGHT}{filename}{Style.RESET_ALL} "
                          f"{Fore.GREEN}was successfully deleted from directory{Style.RESET_ALL} "
                          f"{Fore.BLUE + Style.BRIGHT}{directory}{Style.RESET_ALL}")
                except OSError as e:
                    failed_deleted_files[filename] = file_size
                    print(f"{file_counter}. {Fore.RED}Failed to deleted file{Fore.RESET} "
                          f"{Fore.BLUE}{filename}{Fore.RESET} "
                          f"{Fore.RED}- {e.strerror} ({e.errno}).{Fore.RESET}")
                    if e.errno == 13:
                        print(f"{Fore.RED}The file is read-only, "
                              f"check file properties and try deleting again.{Fore.RESET}")
                    else:
                        print(f"Unknown Error, need to add error code")

                file_counter += 1

        # elapsed time
        elapsed_time = time.time() - start_time
        formatted_time = choose_action.format_elapsed_time(elapsed_time)

        deleted_files_count = len(success_deleted_files)
        msg1_for_1 = f"\n{Fore.GREEN + Style.BRIGHT}Deleting files completed successfully!{Style.RESET_ALL} " \
                     f"{Fore.BLUE}{deleted_files_count}{Fore.RESET} " \
                     f"{Fore.GREEN + Style.BRIGHT}file were deleted.{Style.RESET_ALL}"
        msg2_for_any = f"\n{Fore.GREEN + Style.BRIGHT}Deleting files completed successfully!{Style.RESET_ALL} " \
                       f"{Fore.BLUE}{deleted_files_count}{Fore.RESET} " \
                       f"{Fore.GREEN + Style.BRIGHT}files were deleted.{Style.RESET_ALL}"

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write status of deleted files to a file
        deleted_file_path = create_deleted_files_log(failed_deleted_files, success_deleted_files,
                                                     deleted_file_path, formatted_time)

        failed_deleted_files_count = len(failed_deleted_files)
        msg1_for_1 = f"{Fore.BLUE}{failed_deleted_files_count}{Fore.RESET} " \
                     f"{Fore.RED}file failed to delete, check{Fore.RESET} " \
                     f"{Fore.BLUE}{deleted_file_path}{Fore.RESET}"
        msg2_for_any = f"{Fore.BLUE}{failed_deleted_files_count}{Fore.RESET} " \
                       f"{Fore.RED}files failed to delete, check{Fore.RESET} " \
                       f"{Fore.BLUE}{deleted_file_path}{Fore.RESET}"

        if failed_deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

    except FileNotFoundError:
        print(f"{Fore.RED}Directory{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET} "
              f"{Fore.RED}does not exist{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}"
              f"An error occurred while deleting files:"
              f"{Fore.RESET} "
              f"{Fore.LIGHTRED_EX}{str(e)}{Fore.RESET}")


'''
Function for logging

#variables:
*failed_deleted_files - file path for unsuccessfully renamed files
*success_deleted_files - dictionary of successfully deleted files
*deleted_file_path - file path for delete file
'''


def create_deleted_files_log(failed_deleted_files, success_deleted_files, deleted_file_path, elapsed_time):
    # create a new file (failed deleted files(count).txt)
    # if such a file is already contained in the directory
    count = 1
    name_of_deleted_file = os.path.splitext(deleted_file_path)[0]
    while os.path.exists(deleted_file_path):
        count += 1
        deleted_file_path = os.path.abspath(os.path.join(os.path.dirname(deleted_file_path),
                                                         f"{name_of_deleted_file}({count}).txt"))

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
        f.write(f"Total size of deleted files: {total_size}\n")
        # elapsed time
        f.write(f"Elapsed time: {elapsed_time} ms.\n\n")

        # const for msg in file
        unsuccessful_delete_msg = f'Unsuccessful deleted {len(failed_deleted_files)}:'
        unsuccessful_delete_msg_len = len(unsuccessful_delete_msg)

        successful_delete_msg = f'Successful deleted {len(success_deleted_files)}:'
        successful_delete_msg_len = len(successful_delete_msg)

        # write list of failed deleted files
        if failed_deleted_files:
            f.write(f'\n{cnst.hash_symbol * (unsuccessful_delete_msg_len + cnst.four_spaces)}')
            f.write(f"\n{cnst.hash_symbol} {unsuccessful_delete_msg} {cnst.hash_symbol}")
            f.write(f'\n{cnst.hash_symbol * (unsuccessful_delete_msg_len + cnst.four_spaces)}\n\n')
            # add a number to each line of the list of failed deleted
            for i, (file, file_size) in enumerate(failed_deleted_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all files deleted successfully
        elif success_deleted_files and not failed_deleted_files:
            f.write(f'\n{cnst.hash_symbol * (cnst.great_job_delete_msg_len + cnst.four_spaces)}')
            f.write(f'\n{cnst.hash_symbol} {cnst.great_job_delete_msg} {cnst.hash_symbol}')
            f.write(f'\n{cnst.hash_symbol * (cnst.great_job_delete_msg_len + cnst.four_spaces)}')
        # write msg if extension does not found in directory
        else:
            f.write(f'\n{cnst.hash_symbol * (cnst.file_not_found_ext_msg_len + cnst.four_spaces)}')
            f.write(f'\n{cnst.hash_symbol} {cnst.file_not_found_ext_msg} {cnst.hash_symbol}')
            f.write(f'\n{cnst.hash_symbol * (cnst.file_not_found_ext_msg_len + cnst.four_spaces)}')

        # write list of successfully deleted files
        if success_deleted_files:
            f.write(f'\n\n{cnst.hash_symbol * (successful_delete_msg_len + cnst.four_spaces)}')
            f.write(f"\n{cnst.hash_symbol} {successful_delete_msg} {cnst.hash_symbol}")
            f.write(f'\n{cnst.hash_symbol * (successful_delete_msg_len + cnst.four_spaces)}\n\n')
            # add a number to each line of the list of successful deleted
            for i, (file, file_size) in enumerate(success_deleted_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return deleted_file_path
