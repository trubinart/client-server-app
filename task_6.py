with open('test_file.txt', "r") as f:
    print(f)

with open('test_file.txt', "r", encoding='utf-8') as f:
    for i in f:
        print(i)