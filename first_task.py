import xml.etree.ElementTree as ET
from shutil import copy2
import os


def create_xml_config_file(file_name):
    """
    Func. creates an XML file based on sample in test tas
    This is not a universal function, it is designed for a specific task
    :param file_name: name for config XML-file.
    """

    root = ET.Element('config')  # Create root tag
    file_tag = ET.SubElement(root, 'file',

                             attrib={
                                    'source_path': 'C:\Windows\system32',
                                     'destination_path': 'C:\Program files',
                                     'file_name': 'kernel32.dll'
                                     })   # Create a child tag with parameters, inherit from root

    file_tag = ET.SubElement(root, 'file',
                             attrib={
                                    'source_path': '/var/log',
                                     'destination_path': '/etc',
                                     'file_name': 'auth.log'
                                     })

    file = ET.ElementTree(root)
    file.write(file_name, encoding="utf-8", xml_declaration=True)   # save to file


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
        print('[WARRING] file "example.xml" not found and was created.')
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
    for child_of_root in root.iter("file"):  # iter method - returns data by the filter in parentheses
        yield child_of_root.attrib  # attrib - Returns the XML attributes of a tag


def copy_func(data):

    """
    Func. copies files based on data-var.
    This is not a universal function, it is designed for a specific task
    :param data: parsed xml data in dict type
    """

    print()
    print('[INFO] copy attempt by config:')
    print(f'[INFO] {data}')

    try:

        copy2(os.path.join(data['source_path'], data['file_name']), data['destination_path'])

        print('[INFO] copying completed.')
    except FileNotFoundError:
        print('[ERROR] File or path not found or incorrect.')
    except PermissionError:
        print('[ERROR] Access denied. Run the code with read permissions for the files.')


if __name__ == '__main__':

    file_name = 'example.xml'   # name for config-file

    parsingData = parsing_xml_config_file(file_name)    # parsing-func, return generator

    for data in parsingData:
        copy_func(data)     # Copy files with data

    input()
