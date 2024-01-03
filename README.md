# File extension changer

## Description: 
**filext_changer.py** - script to change file extension .!ut to .part and vice versa.
It also allows you to delete files of a certain extension or remove the extension from files.

## Libraries:
1. os (for os functions)
2. datetime (for time functions)
3. colorama (for color functions)
4. time (for time functions)

## Files of program
1. main.py - main function
2. choose_action.py - function for choose action
3. delete_files.py - function for delete files
4. rename_files.py - function for rename files
5. remove_files.py - function for remove files
6. add_extension_to_empty_files - appends an extension to a file without an extension
7. add_ext_to_ext - adds an extension to an existing extension
8. create_files_test.py - function for create files
9. test_choose_action.py - function for unit tests
10. main_config.py - config file for ease of use from the file
11. extensions_config.py - configuration file for file extensions

## Measured time:
1. Deletion of a million files occurs in 4 minutes
2. Renaming a million files in 8 minutes

## Feature List:
- [x] Change file extension `.!ut` to `.part` and vice versa.
- [x] Saving success renaming and failed renaming attempts and date to `deleted files.txt`.
- [x] Deleting files with extension `.!ut` || `.part`.
- [x] Removing extension `.!ut` || `.part`.
- [x] Adding extension `.!ut` || `.part` to files without extension.
- [x] Add extension to files with specific extension(`.txt`, `.jpg` etc.).

## Example files:
### Deleted files.txt
```
Current date: Wed 2024-01-03 13:54:14 PM
Current directory: C:\Users\Username\Documents
Total deleted files: 0
Total failed deleted files: 2
Total size of deleted files: 0.00 bytes
Elapsed time: 00:00:00.003 ms.

###########################
# Unsuccessful deleted 2: #
###########################
1. file1.txt.!ut 5 kb
2. file2.txt.!ut 5 kb
```

## Screenshot of the program
- Rename files with a specific extension  
![Rename files example](https://github.com/awerty1/filext_changer/blob/1194c5f64ee153f8f33b9d4adaf267ed4b0fcede/2023-05-14_13-47-01.png)
- Delete files with a specific extension
![Delete files example](https://github.com/awerty1/filext_changer/blob/4b87a486597fc8815d287d0d04eccfd14432ce6b/2023-05-14_17-38-46.png)
- Remove files extensions from the directory
![Remove file extension example](https://github.com/awerty1/filext_changer/blob/b2d15f3673f0c46980f1548f7077d3986155a786/img/2023-05-21_22-25-01.png)
- Add extension to empty file
![Add extension to empty file example](https://github.com/awerty1/filext_changer/blob/a83961734dd0c4408b5da3c11599df257baa2c4a/img/2023-05-25_21-12-00.png)
- Add extension to file with specific extension
![Add extension to file with specific extension example](https://github.com/awerty1/filext_changer/blob/b738e34b803d91ab73812ff30cc812e95e3a2999/img/2023-05-28_15-37-12.png)

