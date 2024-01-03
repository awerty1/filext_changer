import os
import time
from datetime import datetime

from colorama import init, Fore, Style

import choose_action

# We call this function to enable color support in the terminal.
init()

'''
Function to add an extension to an existing extension

#variables
*directory - the directory to search for files
*add_extension_to_file - the file extension to add (e.g., ".txt")
*add_filext_path - file path for added extension to extension files
'''


def add_ext_to_ext(directory: str, add_extension_to_file: str, add_filext_path: str) -> None:
    start_time = time.time()
    file_counter = 1
    success_add_ext_to_files = {}
    failed_add_ext_to_files = {}
    ext_search = choose_action.get_valid_extension_to_add_function()
    try:
        print(f"\n{Fore.LIGHTWHITE_EX}"
              f"Adding file extensions occurs in the directory:"
              f"{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET}")

        # Iterate over all files in a directory
        for filename in os.listdir(directory):
            # Check that the file has extension
            if filename.lower().endswith(ext_search):
                filepath = os.path.join(directory, filename)
                file_size = os.path.getsize(filepath)
                try:
                    # Create a new filename with an extension added
                    old_path = os.path.join(directory, filename)
                    new_filename = filename + add_extension_to_file
                    new_path = os.path.join(directory, new_filename)
                    os.rename(old_path, new_path)
                    new_path_basename = os.path.basename(new_filename)

                    success_add_ext_to_files[filename] = file_size
                    print(f"{file_counter}. "
                          f"{Fore.GREEN}To file{Fore.RESET} "
                          f"{Fore.WHITE}{filename}{Fore.RESET}"
                          f" {Fore.GREEN}was added extension successfully{Fore.RESET} "
                          f"{Fore.BLUE + Style.BRIGHT}{new_path_basename}{Style.RESET_ALL}")
                except FileExistsError:
                    failed_add_ext_to_files[filename] = file_size
                    print(f"{file_counter}. "
                          f"{Fore.RED}Failed to add extension to file{Fore.RESET} "
                          f"{Fore.LIGHTRED_EX}{filename}{Fore.RESET}")

                file_counter += 1

        # elapsed time
        elapsed_time = time.time() - start_time
        formatted_time = choose_action.format_elapsed_time(elapsed_time)

        deleted_files_count = len(success_add_ext_to_files)
        msg1_for_1 = f"\n{Fore.GREEN}Added file extension completed successfully!{Fore.RESET} " \
                     f"{Fore.BLUE}{deleted_files_count}{Fore.RESET} " \
                     f"{Fore.GREEN}file were added.{Fore.RESET}"
        msg2_for_any = f"\n{Fore.GREEN}Added files extensions completed successfully!{Fore.RESET} " \
                       f"{Fore.BLUE}{deleted_files_count}{Fore.RESET} " \
                       f"{Fore.GREEN}files extension were added.{Fore.RESET}"

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write status of deleted files to a file
        add_filext_path = create_add_ext_files_log(failed_add_ext_to_files, success_add_ext_to_files,
                                                   add_filext_path, formatted_time)

        failed_deleted_files_count = len(failed_add_ext_to_files)
        msg1_for_1 = f"{Fore.BLUE}{failed_deleted_files_count}{Fore.RESET} " \
                     f"{Fore.RED}file failed to add extension, check{Fore.RESET} " \
                     f"{Fore.BLUE}{add_filext_path}{Fore.RESET}"
        msg2_for_any = f"{Fore.BLUE}{failed_deleted_files_count}{Fore.RESET} " \
                       f"{Fore.RED}files failed to add extension, check{Fore.RESET} " \
                       f"{Fore.BLUE}{add_filext_path}{Fore.RESET}"

        if failed_deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)
    except FileNotFoundError:
        print(f"{Fore.RED}Directory{Fore.RESET} "
              f"{Fore.BLUE}{directory}{Fore.RESET} "
              f"{Fore.RED}does not exist{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while added extension to file:{Fore.RESET} "
              f"{Fore.LIGHTRED_EX}{str(e)}{Fore.RESET}")


'''
Function for saving information about operations to a file

#variables:
*failed_remove_ext_frm_files 
*success_remove_ext_frm_files
*remove_filext_path
*elapsed_time
'''


def create_add_ext_files_log(failed_added_ext_to_files: dict[str, int],
                             success_add_ext_to_files: dict[str, int],
                             add_filext_path: str, elapsed_time: str) -> str:
    # create a new file (failed deleted files(count).txt)
    # if such a file is already contained in the directory
    count = 1
    name_of_file_without_extension = os.path.splitext(add_filext_path)[0]
    while os.path.exists(add_filext_path):
        count += 1
        add_filext_path = os.path.abspath(os.path.join(os.path.dirname(add_filext_path),
                                                       f"{name_of_file_without_extension}({count}).txt"))
    now = datetime.now()
    # format date as string e.g. "Sat 2023-05-13 17:12:36 PM"
    date_string = now.strftime("%a %Y-%m-%d %H:%M:%S %p %Z")
    # total size of deleted files
    total_size = sum(success_add_ext_to_files.values())
    total_size = choose_action.format_size(total_size)

    # write list of "unsuccessful deleted" of files
    with open(add_filext_path, "w") as f:
        # write date followed by new line
        f.write("Current date: " + date_string + "\n")
        # write current directory
        f.write("Current directory: " + os.path.dirname(add_filext_path) + "\n")
        # count of all deleted files
        f.write(f"Total removed extension files: {len(success_add_ext_to_files)}\n")
        # count of failed deleted files
        f.write(f"Total failed removed extension files: {len(failed_added_ext_to_files)}\n")
        # total size of deleted files
        f.write(f"Total size of removed extension files: {total_size}\n")
        # elapsed time
        f.write(f"Elapsed time: {elapsed_time} ms.\n\n")

        # write list of failed extension added to file
        if failed_added_ext_to_files:
            f.write('\n############################################')
            f.write(f"\n# Unsuccessful added extension {len(failed_added_ext_to_files)}: #")
            f.write('\n############################################\n\n')
            # add a number to each line of the list of failed added extension
            for i, (file, file_size) in enumerate(failed_added_ext_to_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all file extensions added successfully
        elif success_add_ext_to_files and not failed_added_ext_to_files:
            f.write('\n#####################################################')
            f.write('\n# Great job! All file extension added successfully! #')
            f.write('\n#####################################################')
        # write msg if extension does not found in directory
        else:
            f.write('\n#######################################')
            f.write('\n# Files not found, no such extension! #')
            f.write('\n#######################################')

        # write list of successfully added files extensions
        if success_add_ext_to_files:
            f.write('\n\n################################################')
            f.write(f"\n# Successful added extension to empty files {len(success_add_ext_to_files)}: #")
            f.write('\n################################################\n\n')
            # add a number to each line of the list of successful added extensions
            for i, (file, file_size) in enumerate(success_add_ext_to_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return add_filext_path
