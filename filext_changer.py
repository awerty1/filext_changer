import os

'''
Function to validate the input of the correct file extension 
Accepts extensions '.!ut' & '.part'
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
A function that renames the extension ".! ut" to ".part" or vice versa
directory - сurrent directory
ext - file extension
'''


def rename_files(directory, extension):
    try:
        counter = 0
        counter_minus = 0
        for filename in os.listdir(directory):
            if not filename.endswith(extension):
                continue

            old_filename = os.path.join(directory, filename)
            root, _ = os.path.splitext(old_filename)
            new_extension = '.part' if extension == '.!ut' else '.!ut'
            new_filename = root + new_extension
            if os.path.exists(new_filename):
                print(f"{counter + 1} \"{new_filename}\" - already exists, skipping")
                counter += 1
                counter_minus += 1
            else:
                os.rename(old_filename, new_filename)
                print(f"{counter + 1} \"{filename}\" was renamed to \"{new_filename}\"")
                counter += 1

        counter -= counter_minus
        print(f"File extension replacement completed successfully! {counter} files were renamed.")
    except FileNotFoundError:
        print(f"Directory \"{directory}\" not found.")
    except OSError:
        print(f"Cannot access directory \"{directory}\".")


if __name__ == '__main__':
    directory = input("Введите путь к директории: ")
    # directory = 'h:/CODE/Python/vogu project/File Extension/'
    extension = get_valid_extension()
    # extension = '.!ut'
    # extension = '.part'
    rename_files(directory, extension.lower())
