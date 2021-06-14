list = ["разработка", "администрирование", "protocol", "standard"]

for i in list:
    encode = i.encode(encoding="utf-8")
    print( f'ENCODE - {encode} / DECODE - {encode.decode("utf-8")} ')
