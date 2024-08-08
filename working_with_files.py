# ASCII и UNICODE (кодировка)
A = []
for i in "Hello human": A.append(ord(i))  # преобразование слова в кодированное число
print("1:", A)
print("2:", [chr(i) for i in range(128)])  # символы из таблицы UNICODE
print("3:", hex(ord("h")))  # преобразование символа в шестнадцатеричный формат
print("4:", type(bb := b"\x68"))  # bytes - байт
print("5:", bb.decode())  # из шестнадцатеричного формата в символьный
