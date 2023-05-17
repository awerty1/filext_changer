import os
import time
from datetime import datetime
# from termcolor import colored
from colorama import init, Fore, Style
import choose_action

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


def rename_files(directory, extension, failed_file_path):
    start_time = time.time()
    try:
        counter = 0
        failed_rename_files = {}
        success_rename_files = {}
        print("")
        print(f"The extension change occurs in the directory "
              f"{Fore.CYAN}{directory}{Fore.RESET}")

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
                print(f"{counter + 1} {Fore.WHITE}{filename}{Fore.RESET} "
                      f"was renamed to "
                      f"{Fore.GREEN + Style.BRIGHT}{new_filename_basename}{Style.RESET_ALL}")
                success_rename_files[filename] = file_size

            counter += 1

        # elapsed time
        elapsed_time = time.time() - start_time
        formatted_time = choose_action.format_elapsed_time(elapsed_time)

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
        failed_file_path = create_rename_file_log(failed_rename_files, success_rename_files,
                                                  failed_file_path, formatted_time)

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
        print(f"Directory {Fore.CYAN}{directory}{Fore.CYAN} not found.")
    except OSError:
        print(f"Cannot access directory {Fore.CYAN}{directory}{Fore.CYAN}.")


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


def create_rename_file_log(failed_rename_files, success_rename_files, failed_file_path, elapsed_time):
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

        # write list of failed files
        if failed_rename_files:
            f.write('\n###########################')
            f.write(f"\n# Unsuccessful renames {len(failed_rename_files)}: #")
            f.write('\n###########################\n\n')
            # add a number to each line of the list of failed renames
            for i, (file, file_size) in enumerate(failed_rename_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
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
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return failed_file_path
