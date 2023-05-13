import os
from datetime import datetime

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
        for filename in os.listdir(directory):
            if not filename.endswith(extension):
                continue

            old_filename = os.path.join(directory, filename)
            root, _ = os.path.splitext(old_filename)
            new_extension = '.part' if extension == '.!ut' else '.!ut'
            new_filename = root + new_extension

            if os.path.exists(new_filename):
                print(f"{counter + 1} \"{new_filename}\" - already exists, skipping")
                failed_rename_files.append(filename)
            else:
                os.rename(old_filename, new_filename)
                print(f"{counter + 1} \"{filename}\" was renamed to \"{new_filename}\"")
                success_rename_files.append(filename)

            counter += 1

        if counter == 1:
            print(f"\nFile extension replacement completed successfully! {counter} file were renamed.")
        else:
            print(f"\nFile extension replacement completed successfully! {counter} files were renamed.")

        # Write filed files to a file
        failed_file_path = rename_with_status_messages(failed_rename_files, success_rename_files, failed_file_path)
        if len(failed_rename_files) == 1:
            print(f"{len(failed_rename_files)} file failed to rename, check {failed_file_path}")
        else:
            print(f"{len(failed_rename_files)} files failed to rename, check {failed_file_path}")
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
        failed_file_path = os.path.abspath(os.path.join(directory, f"Renamed files({count}).txt"))
        count += 1

    now = datetime.now()
    # format date as string
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

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
    rename_files(directory, extension.lower(), failed_file_path)
