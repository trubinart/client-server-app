import csv
import re
import os
from pprint import pprint


def get_data():
    main_list = []
    search_list = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_list.append(search_list)
    file_list = os.listdir(os.getcwd())

    for file in file_list:
        if re.match(f'info', file):
            with open(file, encoding='cp1251') as file:
                string = file.read()
                sistem_production = re.findall(search_list[0] + r".{1,}", string)[0].split('  ')[-1].strip()
                os_name = re.findall(search_list[1] + r".{1,}", string)[0].split('  ')[-1].strip()
                product_code = re.findall(search_list[2] + r".{1,}", string)[0].split('  ')[-1].strip()
                sistem_type = re.findall(search_list[3] + r".{1,}", string)[0].split('  ')[-1].strip()

                data = []
                data.append(sistem_production)
                data.append(os_name)
                data.append(product_code)
                data.append(sistem_type)
                main_list.append(data)

    return main_list


def write_to_csv(file):
    list_to_write = get_data()

    with open(file, 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in list_to_write:
            f_n_writer.writerow(row)

if __name__ == "__main__":
    write_to_csv('result.csv')
