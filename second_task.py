import hashlib
import sqlite3

debug = 0


def create_hash(file_name: str, hash_type):
    """
    Func. returns xml file in project directory
    This is not a universal function, it is designed for a specific task
    :param file_name: name or .
    """

    try:
        open_file = open(file_name, 'r')
    except FileNotFoundError:
        if debug == 1:
            print(f'[ERROR] File {file_name} not found')
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
            print(f'[ERROR] incorrect hash-type for file {file_name}: ({hash_type}). ')
        return

    open_file.close()
    #    print(f'[INFO] hash sum for file "{file_name}": {file_hash.hexdigest()}')

    return file_hash.hexdigest()


def add_hash_info_to_test_file(file_name, hash_type, test_file):

    test_file.write(f'{file_name} {hash_type} {create_hash(file_name, hash_type)} \n')


def check_file(hash_file_path, file_path):
    hash_file = open(hash_file_path, 'r')
    try:
        open(file_path, 'r')
    except FileNotFoundError:
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
    with open('hash_file.txt', 'w+') as test_file:
        add_hash_info_to_test_file('file_01.txt', 'md5', test_file)
        add_hash_info_to_test_file('second_task_folder/file_02.txt', 'md5', test_file)
        add_hash_info_to_test_file('example.xml', 'sha1', test_file)
        add_hash_info_to_test_file('second_task.py', 'sha224', test_file)
        add_hash_info_to_test_file('first_task.py', 'sha256', test_file)
        add_hash_info_to_test_file('file_02.txt', 'sha24', test_file)  # invalid hash type
        add_hash_info_to_test_file('file_04.txt', 'sha224', test_file)  # file does not exist


if __name__ == "__main__":
    print()

    # create_txt_file_with_hash_func()

    print(check_file('hash_file.txt', 'file_01.txt'))
    print(check_file('hash_file.txt', 'second_task_folder/file_02.txt'))
    print(check_file('hash_file.txt', 'example.xml'))
    print(check_file('hash_file.txt', 'second_task.py'))  # will give an error if you change this python file
    print(check_file('hash_file.txt', 'first_task.py'))
    print(check_file('hash_file.txt', 'file_02.txt'))  # the file is not in the directory
    print(check_file('hash_file.txt', 'file_03.txt'))  # the file is not in the hash file
