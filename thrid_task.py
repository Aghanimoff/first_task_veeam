from pathlib import Path
from os import listdir, urandom, remove
from os.path import isfile, join, getsize
from datetime import datetime
import psutil


class Test_Case_Exception(Exception):
    pass


class Test_Case(Test_Case_Exception):

    def __init__(self, tc_id=0, name='default'):
        self.log('Initialization in Test_Case')
        self.tc_id = tc_id
        self.name = name
        self.execute()

    def log(self, message: str = 'null_message', m_type: str = 'i'):

        if m_type.lower() == 'i':
            m_type = 'INFO'
        elif m_type.lower() == 'w':
            m_type = 'WARNING'
        elif m_type.lower() == 'e':
            m_type = 'ERROR'
        elif m_type.lower() == 'f':
            m_type = '!!! FATAL ERROR !!!'
        elif m_type.lower() == 'p':
            print('[Test passed] ' + message)
            return
        else:
            raise ValueError("incorrect m_type identifier")

        print(f'[{m_type}] [datetime: {datetime.now()}] '
              f'[class: {self.__class__.__name__}] '
              f'[{self.__dict__}] '
              f'{message}')

        # заделка на будущие - можно инспектить строку, название метода и путь до файла конфига. Нужен модуль inspect

        # f'[line [{inspect.getlineno(inspect.currentframe())}] func [{inspect.currentframe().f_code.co_name}]'
        # f' in file: {inspect.getsourcefile(inspect.currentframe())}] '

    def prep(self):
        self.log('prep in Test_Case')
        pass

    def run(self):
        self.log('run in Test_Case')
        pass

    def clean_up(self):
        self.log('clean_up in Test_Case')
        pass

    def execute(self):
        try:
            self.log('execute in Test_Case')

            try:
                self.prep()
            except Test_Case_Exception:
                raise Test_Case_Exception('Ошибка в prep')

            try:
                self.run()
            except Test_Case_Exception:
                raise Test_Case_Exception('Ошибка в run')

            try:
                self.clean_up()
            except Test_Case_Exception:
                raise Test_Case_Exception('Ошибка в clean_up')

            self.log(f'{self.__class__.__name__} Passed', 'p')

            pass

        except Test_Case_Exception:
            self.log('Ошибка Test_Case_Exception', 'e')

    def __del__(self):
        self.log('delete in Test_Case')
        print()


class Test_Case_List_Files(Test_Case):

    def __init__(self):
        self.log('Initialization in Test_Case_List_Files')
        self.tc_id = 1
        self.name = 'check_file_list'
        super().__init__(tc_id=self.tc_id, name=self.name)

    def prep(self):
        self.log('prep in Test_Case_List_Files')
        current_time = int(datetime.timestamp(datetime.now()))

        if current_time & 1 == 0:
            self.log(f'prep:   -->    Время с начала эпохи Unix =, {current_time}, чётно, программа продолжит выполнение')
        else:
            self.log(f'prep   -->   Время с начала эпохи Unix =, {current_time}, нечётно, программа прервётся', 'w')
            raise Test_Case_Exception('prep Error')

    def run(self):
        self.log('run in Test_Case_List_Files')

        self.log(f'run   -->   {[i for i in listdir(Path.home()) if isfile(join(Path.home(), i))]}')

        # альтернатива (с путями)
        # self.log(f'run  -->  {list(map(str, sorted(Path.home().glob("*.*"))))}')

    def clean_up(self):
        self.log('clean_up in Test_Case_List_Files')
        self.log('clean_up   -->   Nothing')
        # raise NotImplementedError


class Test_Case_Random_Files(Test_Case):
    TEST_FILE_NAME = 'Test'

    def __init__(self, ram):
        self.log('Initialization in Test_Case_Random_Files')
        self.tc_id = 2
        self.name = 'check_file_random'
        self.ram = ram
        super().__init__(tc_id=self.tc_id, name=self.name)

    def prep(self):
        self.log('prep in Test_Case_Random_Files')
        total_ram = psutil.virtual_memory()[0] / 1024 / 1024

        if total_ram < self.ram:
            self.log(f'prep   -->   {total_ram} гб ОЗУ недостаточно. Наберите хотя бы {self.ram/1024} гб', 'w')
            raise Test_Case_Exception('')

        self.log(f'prep   -->   Текущая память = {total_ram} гб, должно быть больше {self.ram/1024} гб. Тест пройден')

    def run(self):
        self.log('run in Test_Case_Random_Files')

        with open(self.TEST_FILE_NAME, 'wb') as a:
            a.write(urandom(1024*1024))

        self.log(f'run   -->  файл {self.TEST_FILE_NAME} успешно записан')
        self.log(f'run   -->  размер файла {getsize(self.TEST_FILE_NAME)/1024} кб')

    def clean_up(self):
        self.log('clean_up in Test_Case_Random_Files')
        remove(self.TEST_FILE_NAME)
        self.log(f'clean_up   -->   файл {self.TEST_FILE_NAME} удалён')
        # raise NotImplementedError


if __name__ == "__main__":

    Test_Case_List_Files()

    ram = 1024  # минимальный объём памяти в мб
    Test_Case_Random_Files(ram)
