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
        extension = input("Введите тип расширения (например, .!ut или .part): ")
        if extension.lower() in valid_extension:
            return extension
        else:
            print("Ошибка: расширение должно быть '.part' либо '.!ut'")


'''
A function that renames the extension ".! ut" to ".part" or vice versa.

#variables:
*directory - current directory
*extension - file extension
*failed_file_path - 
'''


def rename_files(directory, extension, failed_file_path):
    try:
        counter = 0
        ##counter_minus = 0
        failed_rename_files = []
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
                #counter += 1
                #counter_minus += 1
                failed_rename_files.append(filename)
            else:
                os.rename(old_filename, new_filename)
                print(f"{counter + 1} \"{filename}\" was renamed to \"{new_filename}\"")

            counter += 1

        #counter -= counter_minus
        print(f"\nFile extension replacement completed successfully! {counter} files were renamed.")

        # Write filed files to a file
        failed_renames_files(failed_rename_files)
        if len(failed_rename_files) == 1:
            print(f"{len(failed_rename_files)} file failed to rename, check {failed_file_path}")
        else:
            print(f"{len(failed_rename_files)} files failed to rename, check {failed_file_path}")
    except FileNotFoundError:
        print(f"Directory \"{directory}\" not found.")
    except OSError:
        print(f"Cannot access directory \"{directory}\".")


'''
A function to add information to a file about files that cannot be renamed because they already exist.
The current date and message are also output to the file.

#variables:
*failed_rename_files - list of failed rename files
*date_string - current date
*failed_file_path - path to file
'''


def failed_renames_files(failed_rename_files):
    # create a new file (Failed rename files(count).txt) if such a file is already contained in the directory
    failed_file_path = os.path.abspath(os.path.join(directory, "Failed rename files.txt"))
    count = 1
    while os.path.exists(failed_file_path):
        failed_file_path = os.path.abspath(os.path.join(directory, f"Failed rename files({count}).txt"))
        # failed_file_path = f"{directory}failed rename files({count}).txt"
        count += 1

    # print(f"{failed_file_path}")

    now = datetime.now()
    # Format date as string
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")

    if failed_rename_files:
        # now = datetime.now()
        # date_string = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(failed_file_path, "w") as f:
            # Write date followed by new line
            f.write("Current date " + date_string + "\n")
            # Write list of failed files
            f.write('\n###########################')
            f.write(f"\n# Unsuccessful renames {len(failed_rename_files)}: #")
            f.write('\n###########################\n\n')
            # Add a number to each line of the list of failed renames
            for i, file in enumerate(failed_rename_files, start=1):
                f.write(f"{i}. {file}\n")
                # f.write("\n".join(failed_rename_files))
    else:
        with open(failed_file_path, "w") as f:
            # Write date followed by new line
            f.write("Current date " + date_string + "\n")
            f.write('\n##############################################')
            f.write('\n# Great job! All files renamed successfully! #')
            f.write('\n##############################################')


if __name__ == '__main__':
    directory = input("Введите путь к директории: ")
    # directory = 'h:/CODE/Python/vogu project/File Extension/'
    extension = get_valid_extension()
    # extension = '.!ut'
    # extension = '.part'
    # failed_file_path = input("Enter path to save failed file names: ")
    # failed_file_path = 'h:/CODE/Python/vogu project/File Extension/Failed rename files.txt'
    failed_file_path = os.path.abspath(os.path.join(directory, 'Failed rename files.txt'))
    rename_files(directory, extension.lower(), failed_file_path)
