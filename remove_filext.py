import os
import time
from datetime import datetime

from colorama import init, Fore, Style

import choose_action
import constants as cnst

# We call this function to enable color support in the terminal.
init()

'''
Function to remove file extension

#variables:
*directory - the directory to search for files
*extension_to_remove - the file extension to delete (e.g., ".txt")
*remove_filext_path - file path for removed extension files
'''


def remove_file_extension(directory: str, extension_to_remove: str, remove_filext_path: str) -> None:
    start_time = time.time()
    file_counter = 1
    success_remove_ext_frm_files = {}
    failed_remove_ext_frm_files = {}
    try:
        print(f"\n{Fore.LIGHTWHITE_EX}"
              f"Remove files extensions occurs in the directory:"
              f"{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET}")

        # Iterate over all files in a directory
        for filename in os.listdir(directory):
            # Check that the file has the correct extension
            if filename.lower().endswith(extension_to_remove):
                filepath = os.path.join(directory, filename)
                file_size = os.path.getsize(filepath)
                try:
                    # Create a new filename without extension
                    new_filename = os.path.splitext(filename)[0]
                    # Create a new file path without extension
                    new_path = os.path.join(directory, new_filename)
                    new_path_basename = os.path.basename(new_path)
                    # Rename the file
                    os.rename(os.path.join(directory, filename), new_path)

                    success_remove_ext_frm_files[filename] = file_size
                    print(f"{file_counter}. "
                          f"{Fore.GREEN}From file{Fore.RESET} "
                          f"{Fore.WHITE}{filename}{Fore.RESET}"
                          f" {Fore.GREEN}was successfully removed extension to{Fore.RESET} "
                          f"{Fore.BLUE + Style.BRIGHT}{new_path_basename}{Style.RESET_ALL}")
                except FileExistsError:
                    failed_remove_ext_frm_files[filename] = file_size
                    base_name = os.path.splitext(filename)[0]
                    print(f"{file_counter}. "
                          f"{Fore.RED}Failed to remove extension from file{Fore.RESET} "
                          f"{Fore.BLUE}{filename}{Fore.RESET}"
                          f"{Fore.RED}, file {Fore.RESET}"
                          f"{Fore.BLUE}{base_name}{Fore.RESET} "
                          f"{Fore.RED}exists.{Fore.RESET}")

                file_counter += 1

        # elapsed time
        elapsed_time = time.time() - start_time
        formatted_time = choose_action.format_elapsed_time(elapsed_time)

        deleted_files_count = len(success_remove_ext_frm_files)
        msg1_for_1 = f"\n{Fore.GREEN}Removed file extension completed successfully!{Fore.RESET} " \
                     f"{Fore.BLUE}{deleted_files_count}{Fore.RESET} " \
                     f"{Fore.GREEN + Style.BRIGHT}file were deleted.{Style.RESET_ALL}"
        msg2_for_any = f"\n{Fore.GREEN}Removed files extensions completed successfully!{Fore.RESET} " \
                       f"{Fore.BLUE}{deleted_files_count}{Fore.RESET} " \
                       f"{Fore.GREEN + Style.BRIGHT}files extension were removed.{Style.RESET_ALL}"

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write status of deleted files to a file
        remove_filext_path = create_remove_ext_frm_files_log(failed_remove_ext_frm_files, success_remove_ext_frm_files,
                                                             remove_filext_path, formatted_time)

        failed_deleted_files_count = len(failed_remove_ext_frm_files)
        msg1_for_1 = f"{Fore.BLUE}{failed_deleted_files_count}{Fore.RESET} " \
                     f"{Fore.RED}file failed to remove extension, check{Fore.RESET} " \
                     f"{Fore.BLUE}{remove_filext_path}{Fore.RESET}"
        msg2_for_any = f"{Fore.BLUE}{failed_deleted_files_count}{Fore.RESET} " \
                       f"{Fore.RED}files failed to remove extension, check{Fore.RESET} " \
                       f"{Fore.BLUE}{remove_filext_path}{Fore.RESET}"

        if failed_deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)
    except FileNotFoundError:
        print(f"{Fore.RED}Directory{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET} "
              f"{Fore.RED}does not exist{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while removed files extension:{Fore.RESET} "
              f"{Fore.LIGHTRED_EX}{str(e)}{Fore.RESET}")


'''
Function for logging

#variables:
*failed_remove_ext_frm_files - file path to unsuccessfully remove files extension
*success_remove_ext_frm_files - dictionary of successfully remove files extension
*remove_filext_path - file path to remove file extension
elapsed_time - total file extension removal time
'''


def create_remove_ext_frm_files_log(failed_remove_ext_frm_files: dict[str, int],
                                    success_remove_ext_frm_files: dict[str, int],
                                    remove_filext_path: str, elapsed_time: str) -> str:
    # create a new file (failed deleted files(count).txt)
    # if such a file is already contained in the directory
    count = 1
    name_of_file_without_extension = os.path.splitext(remove_filext_path)[0]
    while os.path.exists(remove_filext_path):
        count += 1
        remove_filext_path = os.path.abspath(os.path.join(os.path.dirname(remove_filext_path),
                                                          f"{name_of_file_without_extension}({count}).txt"))
    now = datetime.now()
    # format date as string e.g. "Sat 2023-05-13 17:12:36 PM"
    date_string = now.strftime("%a %Y-%m-%d %H:%M:%S %p %Z")
    # total size of deleted files
    total_size = sum(success_remove_ext_frm_files.values())
    total_size = choose_action.format_size(total_size)

    # write list of "unsuccessful deleted" of files
    with open(remove_filext_path, "w") as f:
        # write date followed by new line
        f.write("Current date: " + date_string + "\n")
        # write current directory
        f.write("Current directory: " + os.path.dirname(remove_filext_path) + "\n")
        # count of all deleted files
        f.write(f"Total removed extension files: {len(success_remove_ext_frm_files)}\n")
        # count of failed deleted files
        f.write(f"Total failed removed extension files: {len(failed_remove_ext_frm_files)}\n")
        # total size of deleted files
        f.write(f"Total size of removed extension files: {total_size}\n")
        # elapsed time
        f.write(f"Elapsed time: {elapsed_time} ms.\n\n")

        # const for msg in file
        unsuccessful_remove_ext_msg = f'Unsuccessful removed extension {len(failed_remove_ext_frm_files)}:'
        unsuccessful_remove_ext_msg_len = len(unsuccessful_remove_ext_msg)

        successful_removed_ext_msg = f'Successful removed extension {len(success_remove_ext_frm_files)}:'
        successful_removed_ext_msg_len = len(successful_removed_ext_msg)

        # write list of failed deleted files
        if failed_remove_ext_frm_files:
            f.write(f'\n{cnst.hash_symbol * (unsuccessful_remove_ext_msg_len + cnst.four_spaces)}')
            f.write(f"\n{cnst.hash_symbol} {unsuccessful_remove_ext_msg} {cnst.hash_symbol}")
            f.write(f'\n{cnst.hash_symbol * (unsuccessful_remove_ext_msg_len + cnst.four_spaces)}\n\n')
            # add a number to each line of the list of failed deleted
            for i, (file, file_size) in enumerate(failed_remove_ext_frm_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all files deleted successfully
        elif success_remove_ext_frm_files and not failed_remove_ext_frm_files:
            f.write(f'\n{cnst.hash_symbol * (cnst.great_job_remove_msg_len + cnst.four_spaces)}')
            f.write(f'\n{cnst.hash_symbol} {cnst.great_job_remove_msg} {cnst.hash_symbol}')
            f.write(f'\n{cnst.hash_symbol * (cnst.great_job_remove_msg_len + cnst.four_spaces)}')
        # write msg if extension does not found in directory
        else:
            f.write(f'\n{cnst.hash_symbol * (cnst.file_not_found_ext_msg_len + cnst.four_spaces)}')
            f.write(f'\n{cnst.hash_symbol} {cnst.file_not_found_ext_msg} {cnst.hash_symbol}')
            f.write(f'\n{cnst.hash_symbol * (cnst.file_not_found_ext_msg_len + cnst.four_spaces)}')

        # write list of successfully deleted files
        if success_remove_ext_frm_files:
            f.write(f'\n\n{cnst.hash_symbol * (successful_removed_ext_msg_len + cnst.four_spaces)}')
            f.write(f"\n{cnst.hash_symbol} {successful_removed_ext_msg} {cnst.hash_symbol}")
            f.write(f'\n{cnst.hash_symbol * (successful_removed_ext_msg_len + cnst.four_spaces)}\n\n')
            # add a number to each line of the list of successful deleted
            for i, (file, file_size) in enumerate(success_remove_ext_frm_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return remove_filext_path
