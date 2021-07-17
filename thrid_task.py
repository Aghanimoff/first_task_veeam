from pathlib import Path
import time
import os

home_path = Path.home()


class test_case:

    def __init__(self, tc_id, name):
        self.tc_id = tc_id
        self.name = name

    def prep(self):

        if int(time.time()) & 1:
            print('не кратно 2')
        else:
            print('кратно 2')
            print(os.listdir(path=home_path))

    def run(self):
        pass

    def clean_up(self):
        pass


if __name__ == "__main__":

    my_list = ['ноль ', 'один', 'два',
               'три', 'четыре', 'пять']

    print()
    for i in reversed(my_list[::-1]):
        print(i)