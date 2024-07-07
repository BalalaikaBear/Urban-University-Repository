import tkinter as tk  # as - упрощение обращения к библиотеке


def get_values():
    num1 = int(number1_entry.get())  # получить информацию из поля ввода
    num2 = int(number2_entry.get())
    return num1, num2


def insert_values(value):
    answer_entry.delete(0, "end")  # очистить поле ввода ("end" - очистить поле до последнего символа)
    answer_entry.insert(0, value)  # вставить значение в поле ввода


def add():
    num1, num2 = get_values()  # вызов функции get_values с присваиванием переменных
    res = num1 + num2
    insert_values(res)  # вызов функции insert_values с заполнением поля ответа


def sub():
    num1, num2 = get_values()  # вызов функции get_values с присваиванием переменных
    res = num1 - num2
    insert_values(res)  # вызов функции insert_values с заполнением поля ответа


def mul():
    num1, num2 = get_values()  # вызов функции get_values с присваиванием переменных
    res = num1 * num2
    insert_values(res)  # вызов функции insert_values с заполнением поля ответа


def div():
    num1, num2 = get_values()  # вызов функции get_values с присваиванием переменных
    res = num1 / num2
    insert_values(res)  # вызов функции insert_values с заполнением поля ответа


window = tk.Tk()  # создать окно
window.title("Калькулятор")  # название окна
window.geometry("350x350")  # задание размера окна
window.resizable(False, False)  # ограничения на изменение размера окна

# создание кнопок
button_add = tk.Button(window, command=add, text="+", width=2)  # создание виджета (<к чему принадлежит>, command=<название функции>)
button_add.place(x=50, y=150)  # расположение элемента на экране

button_sub = tk.Button(window, command=sub, text="-", width=2)
button_sub.place(x=100, y=150)

button_mul = tk.Button(window, command=mul, text="x", width=2)
button_mul.place(x=150, y=150)

button_div = tk.Button(window, command=div, text="/", width=2)
button_div.place(x=200, y=150)


# поле ввода
number1_entry = tk.Entry(window, width=28)
number1_entry.place(x=50, y=50)

number2_entry = tk.Entry(window, width=28)
number2_entry.place(x=50, y=100)

answer_entry = tk.Entry(window, width=28)
answer_entry.place(x=50, y=200)


# текст
number1 = tk.Label(window, text="Введите первое число:")
number1.place(x=50, y=25)

number2 = tk.Label(window, text="Введите второе число:")
number2.place(x=50, y=75)

number3 = tk.Label(window, text="Ответ:")
number3.place(x=50, y=175)


window.mainloop()  # обновление информации на экране

# для создания exe файла необходимо прописать в консоли: auto-py-to-exe
