import source2 as s2  # задание псевдонима
#from source2 import *  # импортировать все данные из файла
#from source2 import say_hi as hi  # импортировать функцию и задать псевдоним

print("Текст из первого модуля")

print(s2.a)
s2.say_hi()

c = 3

print(s2.__name__, type(s2.__name__))
