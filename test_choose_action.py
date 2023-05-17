import os
from unittest.mock import patch
import pytest
import unittest
from choose_action import enter_directory
from choose_action import choose_action
from choose_action import format_size
from choose_action import format_elapsed_time
from choose_action import get_valid_extension

# здесь описываем тесты
# 1. Проверка, что функция возвращает корректный путь к существующей директории:
def test_enter_directory_existing_dir():
    # используем текущую директорию как существующую
    dir_path = os.getcwd()
    with patch('builtins.input', return_value=dir_path):
        assert enter_directory() == dir_path

'''
# 2. Проверка, что функция вызывает исключение при вводе несуществующего пути:
def test_enter_directory_nonexisting_dir():
    with patch('builtins.input', return_value='h:\\CODE\\Python\\vogu project\\File Extension\\test'):
        with pytest.raises(ValueError, match=r'The entered path does not exist.'):
            enter_directory()


# 3. Проверка, что функция вызывает исключение при вводе пути к файлу, а не к директории:
def test_enter_directory_file_path():
    # используем текущий файл как путь к файлу
    file_path = os.path.realpath(__file__)
    with patch('builtins.input', return_value='h:/CODE/Python/vogu project/File Extension/gfdgdfgd.txt'):
        with pytest.raises(ValueError, match=r'The entered path is not a directory.'):
            enter_directory()
'''


class test_format_elapsed_time(unittest.TestCase):
    def test_format_elapsed_time(self):
        self.assertEqual(format_elapsed_time(3600), "01:00:00.000")
        self.assertEqual(format_elapsed_time(3661.5), "01:01:01.500")
        self.assertEqual(format_elapsed_time(60), "00:01:00.000")
        self.assertEqual(format_elapsed_time(0.5), "00:00:00.500")

class test_format_size(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(format_size(100), "100.00 bytes")
    def test_format_kilobytes(self):
        self.assertEqual(format_size(2048), "2.00 KB")
    def test_format_megabytes(self):
        self.assertEqual(format_size(1048576), "1.00 MB")
    def test_format_gigabytes(self):
        self.assertEqual(format_size(1073741824), "1.00 GB")
    def test_format_terabytes(self):
        self.assertEqual(format_size(1099511627776), "1.00 TB")
    def test_format_petabytes(self):
        self.assertEqual(format_size(1125899906842624), "1.00 PB")
    def test_format_rounding(self):
        self.assertEqual(format_size(50000), "48.83 KB")


class test_get_valid_extension(unittest.TestCase):
    @patch('builtins.input', side_effect=['.part'])
    def test_valid_part_extension(self, mock_input):
        self.assertEqual(get_valid_extension(), '.part')

    @patch('builtins.input', side_effect=['.!ut'])
    def test_valid_ut_extension(self, mock_input):
        self.assertEqual(get_valid_extension(), '.!ut')

    @patch('builtins.input', side_effect=['.txt', '.part'])
    def test_valid_extension_after_invalid_attempt(self, mock_input):
        self.assertEqual(get_valid_extension(), '.part')

    @patch('builtins.input', side_effect=['.t', '.ut', '.jpeg', '.pdf', '.part'])
    def test_valid_extension_after_multiple_invalid_attempts(self, mock_input):
        self.assertEqual(get_valid_extension(), '.part')


if __name__ == '__main__':
    pytest.main()
    unittest.main()
