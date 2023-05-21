import os
import time
from datetime import datetime
# from termcolor import colored
from colorama import init, Fore, Style
import choose_action


def remove_file_extension(directory, extension_to_remove, remove_filext_path):
    start_time = time.time()
    file_counter = 1
    success_remove_ext_frm_files = {}
    failed_remove_ext_frm_files = {}
    try:
        print("")
        print(f"The extension change occurs in the directory "
              f"{Fore.CYAN}{directory}{Fore.RESET}")

        # перебираем все файлы в директории
        for filename in os.listdir(directory):
            # проверяем, что файл имеет нужное расширение
            if filename.endswith(extension_to_remove):
                filepath = os.path.join(directory, filename)
                file_size = os.path.getsize(filepath)
                try:
                    # создаем новое имя файла без расширения
                    new_filename = os.path.splitext(filename)[0]
                    # создаем новый путь к файлу без расширения
                    new_path = os.path.join(directory, new_filename)
                    new_path_basename = os.path.basename(new_path)
                    # переименовываем файл
                    os.rename(os.path.join(directory, filename), new_path)

                    success_remove_ext_frm_files[filename] = file_size
                    print(f"{file_counter}. File "
                          f"{Fore.GREEN + Style.BRIGHT}{filename}{Style.RESET_ALL} "
                          f"was successfully removed extension to "
                          f"{Fore.CYAN}{new_path_basename}{Fore.RESET}")
                except FileExistsError:
                    failed_remove_ext_frm_files[filename] = file_size
                    print(f"{file_counter}. Failed to remove extension from file "
                          f"{Fore.LIGHTRED_EX}{filename}{Fore.RESET}")

                file_counter += 1

        # elapsed time
        elapsed_time = time.time() - start_time
        formatted_time = choose_action.format_elapsed_time(elapsed_time)

        deleted_files_count = len(success_remove_ext_frm_files)
        msg1_for_1 = f"\nDeleting files completed successfully! " \
                     f"{deleted_files_count} file were deleted."
        msg2_for_any = f"\nDeleting files completed successfully! " \
                       f"{deleted_files_count} files were deleted."

        if deleted_files_count == 1:
            print(msg1_for_1)
        else:
            print(msg2_for_any)

        # Write status of deleted files to a file
        remove_filext_path = create_remove_ext_frm_files_log(failed_remove_ext_frm_files, success_remove_ext_frm_files,
                                                             remove_filext_path, formatted_time)

        failed_deleted_files_count = len(failed_remove_ext_frm_files)
        msg1_for_1 = f"{failed_deleted_files_count} " \
                     f"file failed to delete, check " \
                     f"{Fore.CYAN}{remove_filext_path}{Fore.RESET}"
        msg2_for_any = f"{failed_deleted_files_count} " \
                       f"files failed to delete, check " \
                       f"{Fore.CYAN}{remove_filext_path}{Fore.RESET}"

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


def create_remove_ext_frm_files_log(failed_remove_ext_frm_files, success_remove_ext_frm_files,
                                    remove_filext_path, elapsed_time):
    # create a new file (failed deleted files(count).txt)
    # if such a file is already contained in the directory
    count = 1
    while os.path.exists(remove_filext_path):
        count += 1
        remove_filext_path = os.path.abspath(os.path.join(os.path.dirname(remove_filext_path),
                                                          f"Removed extension from files({count}).txt"))
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
        f.write(f"Total deleted files: {len(success_remove_ext_frm_files)}\n")
        # count of failed deleted files
        f.write(f"Total failed deleted files: {len(failed_remove_ext_frm_files)}\n")
        # total size of deleted files
        f.write(f"Total size of deleted files: {total_size}\n")
        # elapsed time
        f.write(f"Elapsed time: {elapsed_time} ms.\n\n")

        # write list of failed deleted files
        if failed_remove_ext_frm_files:
            f.write('\n###########################')
            f.write(f"\n# Unsuccessful deleted {len(failed_remove_ext_frm_files)}: #")
            f.write('\n###########################\n\n')
            # add a number to each line of the list of failed deleted
            for i, (file, file_size) in enumerate(failed_remove_ext_frm_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
        # write msg is all files deleted successfully
        elif success_remove_ext_frm_files and not failed_remove_ext_frm_files:
            f.write('\n##############################################')
            f.write('\n# Great job! All files deleted successfully! #')
            f.write('\n##############################################')
        # write msg if extension does not found in directory
        else:
            f.write('\n#######################################')
            f.write('\n# Files not found, no such extension! #')
            f.write('\n#######################################')

        # write list of successfully deleted files
        if success_remove_ext_frm_files:
            f.write('\n\n#########################')
            f.write(f"\n# Successful deleted {len(success_remove_ext_frm_files)}: #")
            f.write('\n#########################\n\n')
            # add a number to each line of the list of successful deleted
            for i, (file, file_size) in enumerate(success_remove_ext_frm_files.items(), start=1):
                file_label = choose_action.format_size(file_size)
                f.write(f"{i}. {file}  {file_label}\n")
    return remove_filext_path
