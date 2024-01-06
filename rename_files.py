import os
import time
from datetime import datetime

from colorama import init, Fore, Style

import choose_action
import constants as cnst

# We call this function to enable color support in the terminal.
init()

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


def rename_files(directory: str, extension: str, failed_file_path: str) -> None:
    start_time = time.time()
    file_counter = 1
    failed_rename_files = {}
    success_rename_files = {}
    try:
        print(f"\n{Fore.LIGHTWHITE_EX}"
              f"The extension change occurs in the directory:"
              f"{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET}")

        for filename in os.listdir(directory):
            if not filename.lower().endswith(extension):
            #if not filename.endswith(extension) and not filename.upper().endswith(extension):
                #print("well done!")
                continue

            old_filename = os.path.join(directory, filename)
            root, _ = os.path.splitext(old_filename)

            new_extension = '.part' if extension == '.!ut' else '.!ut'
            #new_extension = '.part' if filename.upper().endswith('.!UT') else '.!ut'

            new_filename = root + new_extension
            new_filename_basename = os.path.basename(new_filename)
            file_size = os.path.getsize(old_filename)

            if os.path.exists(new_filename):
                print(f"{file_counter}. {Fore.BLUE + Style.BRIGHT}{new_filename_basename}{Style.BRIGHT} "
                      f"{Fore.RED}- already exists, skipping{Fore.RESET}")
                failed_rename_files[filename] = file_size
            else:
                os.rename(old_filename, new_filename)
                print(f"{file_counter}. {Fore.WHITE}{filename}{Fore.RESET}"
                      f" {Fore.GREEN + Style.BRIGHT}was renamed to{Style.RESET_ALL} "
                      f"{Fore.BLUE + Style.BRIGHT}{new_filename_basename}{Style.RESET_ALL}")
                success_rename_files[filename] = file_size

            file_counter += 1

        # elapsed time
        elapsed_time = time.time() - start_time
        formatted_time = choose_action.format_elapsed_time(elapsed_time)

        success_rename_files_count = len(success_rename_files)
        msg1_for_1 = f"\n{Fore.GREEN + Style.BRIGHT}" \
                     f"File extension replacement completed successfully!" \
                     f"{Style.RESET_ALL}" \
                     f" {Fore.BLUE}{success_rename_files_count}{Fore.RESET} " \
                     f"{Fore.GREEN + Style.BRIGHT}file were renamed.{Style.RESET_ALL}"
        msg2_for_any = f"\n{Fore.GREEN + Style.BRIGHT}" \
                       f"File extension replacement completed successfully!" \
                       f"{Style.RESET_ALL}" \
                       f" {Fore.BLUE}{success_rename_files_count}{Fore.RESET} " \
                       f"{Fore.GREEN + Style.BRIGHT}files were renamed.{Style.RESET_ALL}"

        if success_rename_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write filed files to a file
        failed_file_path = create_rename_file_log(failed_rename_files, success_rename_files,
                                                  failed_file_path, formatted_time)

        failed_rename_files_count = len(failed_rename_files)
        msg1_for_1 = f"{Fore.BLUE}{failed_rename_files_count}{Fore.RESET} " \
                     f"{Fore.RED}file failed to rename, check{Fore.RESET} " \
                     f"{Fore.BLUE}{failed_file_path}{Fore.RESET}"
        msg2_for_any = f"{Fore.BLUE}{failed_rename_files_count}{Fore.RESET} " \
                       f"{Fore.RED}files failed to rename, check{Fore.RESET} " \
                       f"{Fore.BLUE}{failed_file_path}{Fore.RESET}"

        if failed_rename_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

    except FileNotFoundError:
        print(f"{Fore.RED}Directory{Fore.RESET} "
              f"{Fore.RED}{directory}{Fore.RESET} "
              f"{Fore.RED}not found.{Fore.RESET}")
    except OSError:
        print(f"{Fore.RED}Cannot access directory{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET}.")


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


def create_rename_file_log(failed_rename_files, success_rename_files,
                           failed_file_path, elapsed_time) -> str:
    # create a new file (failed rename files(count).txt) if such a file is already contained in the directory
    count = 1
    name_of_renamed_file = os.path.splitext(failed_file_path)[0]
    while os.path.exists(failed_file_path):
        count += 1
        failed_file_path = os.path.abspath(os.path.join(os.path.dirname(failed_file_path),
                                                        f"{name_of_renamed_file}({count}).txt"))

    now = datetime.now()
    # format date as string e.g. "Sat 2023-05-13 17:12:36 PM"
    date_string = now.strftime("%a %Y-%m-%d %H:%M:%S %p %Z")
    # size of success renamed
    total_size = sum(success_rename_files.values())
    total_size = choose_action.format_size(total_size)

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
        f.write(f"Total size of renamed files: {total_size}\n")
        # elapsed time
        f.write(f"Elapsed time: {elapsed_time} ms.\n\n")

        # const for msg in file
        unsuccessful_rename_msg = f'Unsuccessful renames {len(failed_rename_files)}:'
        unsuccessful_rename_msg_len = len(unsuccessful_rename_msg)

        successful_rename_msg = f'Successful renames {len(success_rename_files)}:'
        successful_rename_msg_len = len(successful_rename_msg)

        # write list of failed files
        if failed_rename_files:
            f.write(f'\n{cnst.hash_symbol * (unsuccessful_rename_msg_len + cnst.four_spaces)}')
            f.write(f"\n{cnst.hash_symbol} {unsuccessful_rename_msg} {cnst.hash_symbol}")
            f.write(f'\n{cnst.hash_symbol * (unsuccessful_rename_msg_len + cnst.four_spaces)}\n\n')
            # add a number to each line of the list of failed renames
            for i, (file, file_size) in enumerate(failed_rename_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all files rename successfully
        elif success_rename_files and not failed_rename_files:
            f.write(f'\n{cnst.hash_symbol * (cnst.great_job_rename_msg_len + cnst.four_spaces)}')
            f.write(f'\n{cnst.hash_symbol} {cnst.great_job_rename_msg} {cnst.hash_symbol}')
            f.write(f'\n{cnst.hash_symbol * (cnst.great_job_rename_msg_len + cnst.four_spaces)}')
        # write msg if extension does not found in directory
        else:
            f.write(f'\n{cnst.hash_symbol * (cnst.file_not_found_ext_msg_len + cnst.four_spaces)}')
            f.write(f'\n{cnst.hash_symbol} {cnst.file_not_found_ext_msg} {cnst.hash_symbol}')
            f.write(f'\n{cnst.hash_symbol * (cnst.file_not_found_ext_msg_len + cnst.four_spaces)}')

        # write list of successfully renamed files
        if success_rename_files:
            f.write(f'\n\n{cnst.hash_symbol * (successful_rename_msg_len + cnst.four_spaces)}')
            f.write(f"\n{cnst.hash_symbol} {successful_rename_msg} {cnst.hash_symbol}")
            f.write(f'\n{cnst.hash_symbol * (successful_rename_msg_len + cnst.four_spaces)}\n\n')
            # add a number to each line of the list of successful renames
            for i, (file, file_size) in enumerate(success_rename_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return failed_file_path
