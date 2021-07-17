import xml.etree.ElementTree as ET
from shutil import copy2
import os


def create_xml_config_file(file_name):
    """
    Func. creates an XML file based on sample in test tas
    This is not a universal function, it is designed for a specific task
    :param file_name: name for config XML-file.
    """

    root = ET.Element('config')  # Создаём главный тэг
    file_tag = ET.SubElement(root, 'file',

                             attrib={
                                    'source_path': 'C:\Windows\system32',
                                     'destination_path': 'C:\Program files',
                                     'file_name': 'kernel32.dll'
                                     })   # Создаём дочерний тэг с параметрами, наследуемся от root

    file_tag = ET.SubElement(root, 'file',
                             attrib={
                                    'source_path': '/var/log',
                                     'destination_path': '/etc',
                                     'file_name': 'auth.log'
                                     })

    file = ET.ElementTree(root)
    file.write(file_name, encoding="utf-8", xml_declaration=True)   # Сохраняем в файл


def get_xml_config_file(file_name):
    """
    Func. returns xml file in project directory
    This is not a universal function, it is designed for a specific task
    :param file_name: name of config XML-file.
    """

    try:
        return open(file_name, "r")

    except FileNotFoundError:
        create_xml_config_file(file_name)
        print('[WARRING] файл "example.xml" не был найден и был создан.')
        return open(file_name, "r")


def parsing_xml_config_file(file_name='example.xml'):
    """
    Func. return one generator iteration with data from xml file
    this is not a universal function, it is designed for a specific task
    :param file_name: name for config XML-file.
    """

    file = get_xml_config_file(file_name)

    tree = ET.ElementTree(file=file)
    root = tree.getroot()
    for child_of_root in root.iter("file"):  # метод iter - возвращает данные по фильтру в скобках
        yield child_of_root.attrib  # attrib - возвращает XML-атрибуты тега


def copy_func(data):

    """
    Func. copies files based on data-var.
    This is not a universal function, it is designed for a specific task
    :param data: parsed xml data in dict type
    """

    print()
    print('[INFO] Попытка копирования по конфигу:')
    print(f'[INFO] {data}')

    try:
        copy2(os.path.join(data['source_path'], data['file_name']), data['destination_path'])
        print('[INFO] Копирование успешно завершено.')
    except FileNotFoundError:
        print('[ERROR] Файл или путь не найдены или заданы некорректно.')
    except PermissionError:
        print('[ERROR] Отказано в доступе. Запустите код с правами на чтение указанных файлов.')
    except Exception:
        print('[ERROR] Непонятная ошибка при попытке копирования файла. ')


if __name__ == '__main__':

    file_name = 'example.xml'   # Задаём имя конфиг-файла

    parsingData = parsing_xml_config_file(file_name)    # Вызываем парсинг-функцию, возвращающую генератор

    for data in parsingData:    # Проходимся по генератору
        copy_func(data)     # Копируем файлы

    input()
