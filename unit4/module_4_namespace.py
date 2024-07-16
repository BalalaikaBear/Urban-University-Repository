def test_function():
    name = test_function.__name__
    def inner_function():
        print("Я в области видимости функции", name)

    inner_function()

try:
    inner_function()
except:
    print("Ошибка!")
    test_function()
