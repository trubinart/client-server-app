import yaml

data = {
    'list': [1, 2, 3, 4, 5],
    'int': 190,
    'dict': {
        '1': 'ʫ',
        '2': 'ʬ'
    }
}

with open('file.yaml', 'w') as f_n:
    yaml.dump(data, f_n, default_flow_style=False, allow_unicode = True)

with open('file.yaml') as f_n:
    f_n_content = yaml.load(f_n, Loader=yaml.FullLoader)
    print(f_n_content)
    print(data == f_n_content)