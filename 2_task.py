import sqlite3
import hashlib

debug = 0


def create_hash(file_name, hash_type):
    """
    Func. returns xml file in project directory
    This is not a universal function, it is designed for a specific task
    :param file_name: name or .
    """

    try:
        open_file = open(file_name, 'r')
    except FileNotFoundError:
        if debug == 1:
            print(f'[ERROR] Файл {file_name} не был найден')
        return

    if hash_type == 'md5':
        file_hash = hashlib.md5(open_file.read().encode())
    elif hash_type == 'sha1':
        file_hash = hashlib.sha1(open_file.read().encode())
    elif hash_type == 'sha224':
        file_hash = hashlib.sha224(open_file.read().encode())
    elif hash_type == 'sha256':
        file_hash = hashlib.sha256(open_file.read().encode())
    else:
        if debug == 1:
            print(f'[ERROR] Указан неподдерживаемый вид хэширования для файла {file_name}: ({hash_type}). ')
        return

    open_file.close()
#    print(f'[INFO] Хэш сумма для файла "{file_name}": {file_hash.hexdigest()}')

    return file_hash.hexdigest()


def add_hash_info_to_test_file(file_name, hash_type, test_file):

    test_file.write(f'{file_name} {hash_type} {create_hash(file_name, hash_type)} \n')


def check_file(hash_file_path, file_path):

    hash_file = open(hash_file_path, 'r')
    try:
        open(file_path, 'r')
    except:
        return f'[ERROR] {file_path} NOT FOUND'

    for line in hash_file:
        split_line = line.split()

        if split_line[0] == file_path:

            if split_line[2] == 'None':
                return f'[ERROR] {file_path} FAIL, incorrect hash sum'

            elif create_hash(file_path, split_line[1]) == split_line[2]:
                return f'[INFO] {file_path} OK'

            else:
                # print(create_hash(file_path, split_line[1]))
                return f'[ERROR] {file_path} FAIL'

    return f'[ERROR] {file_path} FILE NOT FOUND IN HASH_FILE'


def create_txt_file_with_hash_func():

    with open('test_file.txt', 'w+') as test_file:

        add_hash_info_to_test_file('file_01.txt', 'md5', test_file)
        add_hash_info_to_test_file('example.xml', 'sha1', test_file)
        add_hash_info_to_test_file('2_task.py', 'sha224', test_file)
        add_hash_info_to_test_file('1_task.py', 'sha256', test_file)
        add_hash_info_to_test_file('file_02.txt', 'sha24', test_file)  # неверный тип хэш-функции
        add_hash_info_to_test_file('file_04.txt', 'sha224', test_file)  # файла не существует


if __name__ == "__main__":

    print()

    # create_txt_file_with_hash_func()

    print(check_file('test_file.txt', 'file_01.txt'))
    print(check_file('test_file.txt', 'example.xml'))
    print(check_file('test_file.txt', '2_task.py'))  # выдаст ошибку, если изменить этот python файл
    print(check_file('test_file.txt', '1_task.py'))
    print(check_file('test_file.txt', 'file_02.txt'))  # файла нет в директории
    print(check_file('test_file.txt', 'file_03.txt'))  # файла нет в хэш-файле
